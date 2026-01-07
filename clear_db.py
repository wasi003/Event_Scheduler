from app import app, db

if __name__ == '__main__':
    with app.app_context():
        confirm = input('This will DROP ALL TABLES and recreate them (data will be lost). Proceed? (yes/no): ')
        if confirm.lower() == 'yes':
            db.drop_all()
            db.create_all()
            print('Database cleared and schema recreated.')
        else:
            print('Aborted.')
