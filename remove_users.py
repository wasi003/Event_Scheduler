from app import app, db
from models import User, Event

if __name__ == '__main__':
    with app.app_context():
        confirm = input('This will DELETE ALL users and clear event ownership. Proceed? (yes/no): ')
        if confirm.lower() != 'yes':
            print('Aborted.')
        else:
            try:
                # Clear ownership on events
                Event.query.update({Event.user_id: None})
                db.session.commit()

                # Delete all users
                num = User.query.delete()
                db.session.commit()

                print(f'Removed {num} users and cleared event ownership.')
            except Exception as e:
                db.session.rollback()
                print('Error:', e)
