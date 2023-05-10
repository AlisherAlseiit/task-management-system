from typing import Annotated


from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..database import get_db
from .. import schemas, oauth2, models, utils
from ..config import settings
from ..crud import users_crud, boards_crud, board_members_crud


router = APIRouter(
    prefix="/boards",
    tags=['board_members']
)


@router.get("/{board_id}/invitations", response_model=list[schemas.BoardMememberOut])
def get_board_members(board_id: int, 
                        db: Annotated[Session, Depends(get_db)], 
                        current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    board = boards_crud.validate_board_presence(db, board_id) 
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value, utils.Roles.MEMBER.value, utils.Roles.OBSERVER.value])
    board_members = board_members_crud.get_board_members(db, board_id)
    return board_members


@router.post("/{board_id}/invitations", status_code=status.HTTP_201_CREATED)
async def send_board_invitations(board_id: int, 
                                    db: Annotated[Session, Depends(get_db)], 
                                    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
                                    invitation_data: schemas.InvitationCreate):
    user = users_crud.get_user_by_email(db, email=invitation_data.recipient_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")
    board = boards_crud.validate_board_presence(db, board_id) 
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value])
    board_member = board_members_crud.get_board_member(db, board_id, user.id)
    if board_member:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already invited to board")
    
    try:
        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
            smtp_server.starttls()
            smtp_server.login(settings.sender_email, settings.sender_password)

            # Create the message object
            message = MIMEMultipart()
            message['Subject'] = 'Invitation to join a board'
            message['From'] = "Task Management App"
            message['To'] = f', {invitation_data.recipient_email}'

            # Create the HTML content of the message
            html = f"<p>You have been invited to join a board.</p><p>Click the following link to accept the invitation: <a href='http://yourapp.com/boards/{board_id}'>http://yourapp.com/boards/{board_id}</a></p>"
            message.attach(MIMEText(html, 'html'))

            # Send the message to the recipients
            smtp_server.sendmail(settings.sender_email, invitation_data.recipient_email, message.as_string())

            # adding member to boardMembers table
            board_members_crud.add_board_member(db, board_id, user.id)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Invitations sent successfully."}


@router.put("/{board_id}/invitations/members/{member_id}", response_model=schemas.BoardMememberOut)
def change_member_role(board_id: int, 
                        db: Annotated[Session, Depends(get_db)],
                        member_id: int,
                        updated_member: schemas.BoardMemberUpdate, 
                        current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    if updated_member.role not in [utils.Roles.ADMIN.value, utils.Roles.MEMBER.value, utils.Roles.OBSERVER.value]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="incorrect role")
    board = boards_crud.validate_board_presence(db, board_id) 
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value])
    board_member = board_members_crud.get_board_member(db, board_id, member_id)
    if not board_member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="board member not found")
    
    board_members_crud.update_board_member(db, board_id, member_id, updated_member)
    return board_member


@router.delete("/{board_id}/invitations/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_board_member(board_id: int, 
                        db: Annotated[Session, Depends(get_db)],
                        member_id: int, 
                        current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    board = boards_crud.validate_board_presence(db, board_id) 
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value])
    board_member = board_members_crud.get_board_member(db, board_id, member_id)
    if not board_member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="board member not found")

    board_members_crud.remove_board_member(db, board_id, user_id=member_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)