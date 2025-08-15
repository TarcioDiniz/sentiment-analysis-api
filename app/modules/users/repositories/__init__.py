import uuid

from app.core.extensions import db
from app.modules.users.models import User

def get_all():
  return User.query.all()

def get_by_id(uid: uuid) -> User | None:
    return db.session.get(User, uid)

def get_by_email(email: str) -> User | None:
    return User.query.filter_by(email=email).first()

def add(u: User) -> User:
    db.session.add(u); db.session.commit(); return u

def remove(u: User):
    db.session.delete(u); db.session.commit()

def paginate(page: int, take: int, search: str | None = None):
    q = User.query
    if search:
        like = f"%{search}%"
        q = q.filter(User.name.ilike(like) | User.email.ilike(like))
    pg = q.order_by(User.id.desc()).paginate(page=page, per_page=take, error_out=False)
    return pg.items, pg.total
