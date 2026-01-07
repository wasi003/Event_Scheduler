from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, date
from functools import wraps

from models import db, User, Event, Resource, EventResourceAllocation

# -------------------------------------------------
# Flask App Configuration
# -------------------------------------------------
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "simple-secret-key"

db.init_app(app)

# -------------------------------------------------
# Home
# -------------------------------------------------
@app.route('/')
def home():
  
        return redirect(url_for('events'))



# -------------------------------------------------
# Login Required Decorator
# -------------------------------------------------
# -------------------------------------------------
# Events
# -------------------------------------------------
@app.route('/events')

def events():
    events = Event.query.all()
    return render_template('events.html', events=events)


@app.route('/profile')

def profile():
    username = session.get('user')
    user = User.query.filter_by(username=username).first()

    user_events = []
    # Try to load events and allocations owned by this user. Be defensive if the model lacks user_id.
    user_events = []
    user_allocations = []
    try:
        if user and hasattr(user, 'user_id'):
            user_events = Event.query.filter_by(user_id=user.user_id).all()
            user_allocations = EventResourceAllocation.query.join(Event).filter(Event.user_id == user.user_id).all()
        else:
            # fallback: no ownership info available on Event model
            user_events = []
            user_allocations = []
    except Exception:
        user_events = []
        user_allocations = []

    return render_template('profile.html', user=user, events=user_events, allocations=user_allocations)


@app.route('/events/add', methods=['GET', 'POST'])

def add_event():
    if request.method == 'POST':
        # Get the current user
        username = session.get('user')
        user = User.query.filter_by(username=username).first()
        
        event = Event(
            title=request.form['title'],
            start_time=datetime.fromisoformat(request.form['start_time']),
            end_time=datetime.fromisoformat(request.form['end_time']),
            description=request.form['description'],
            user_id=user.user_id if user else None  # Set the creator's user_id
        )
        db.session.add(event)
        db.session.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for('events'))

    return render_template('add_event.html')


@app.route('/events/edit/<int:event_id>', methods=['POST'])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    username = session.get('user')
    user = User.query.filter_by(username=username).first()
    
    # Check permissions
    if not user or (user.username != 'admin' and (hasattr(event, 'user_id') and event.user_id != user.user_id)):
        return {"message": "You can only edit your own events!"}, 403

    try:
        event.title = request.form['title']
        event.description = request.form['description']
        event.start_time = datetime.fromisoformat(request.form['start_time'])
        event.end_time = datetime.fromisoformat(request.form['end_time'])
        
        db.session.commit()
        return {"message": "Event updated successfully!"}, 200
    except Exception as e:
        db.session.rollback()
        return {"message": f"Error updating event: {str(e)}"}, 500


@app.route('/events/delete/<int:event_id>', methods=['POST'])

def delete_event_web(event_id):
    """Delete event via web form (session-based auth)"""
    event = Event.query.get_or_404(event_id)
    
    # Get current user
    username = session.get('user')
    user = User.query.filter_by(username=username).first()
    
    # Only event owner or admin can delete
    if user and (user.username == 'admin' or (hasattr(event, 'user_id') and event.user_id == user.user_id)):
        try:
            # Remove allocations first
            EventResourceAllocation.query.filter_by(event_id=event.event_id).delete()
            db.session.delete(event)
            db.session.commit()
            flash("Event deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting event: {str(e)}", "danger")
    else:
        flash("You can only delete your own events!", "danger")
    
    return redirect(url_for('events'))


# -------------------------------------------------
# Resources
# -------------------------------------------------
@app.route('/resources/')

def resources():
    resources = Resource.query.all()
    return render_template('resources.html', resources=resources)


@app.route('/resources/add', methods=['GET', 'POST'])

def add_resource():
    if request.method == 'POST':
        resource = Resource(
            resource_name=request.form['name'],
            resource_type=request.form['type']
        )
        db.session.add(resource)
        db.session.commit()
        flash("Resource added successfully!", "success")
        return redirect(url_for('resources'))

    return render_template('add_resource.html')


@app.route('/resources/edit/<int:resource_id>', methods=['POST'])

def edit_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    resource.resource_name = request.form.get('name', resource.resource_name)
    resource.resource_type = request.form.get('type', resource.resource_type)
    db.session.commit()
    flash("Resource updated successfully!", "success")
    return redirect(url_for('resources'))


@app.route('/resources/delete/<int:resource_id>', methods=['POST'])

def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    db.session.delete(resource)
    db.session.commit()
    flash("Resource deleted successfully!", "success")
    return redirect(url_for('resources'))


# -------------------------------------------------
# Allocation & Conflict Detection
# -------------------------------------------------
@app.route('/allocate', methods=['GET', 'POST'])

def allocate_resource():
    events = Event.query.all()
    resources = Resource.query.all()
    allocations = EventResourceAllocation.query.all()
    error = None

    if request.method == 'POST':
        event_id = int(request.form['event_id'])
        resource_id = int(request.form['resource_id'])
        event = Event.query.get(event_id)

        conflict = (
            EventResourceAllocation.query
            .join(Event)
            .filter(
                EventResourceAllocation.resource_id == resource_id,
                Event.start_time < event.end_time,
                Event.end_time > event.start_time
            ).first()
        )

        if conflict:
            error = "This resource is already booked for another event during this time."
        else:
            allocation = EventResourceAllocation(
                event_id=event_id,
                resource_id=resource_id
            )
            db.session.add(allocation)
            db.session.commit()
            # Reload allocations instead of redirecting
            allocations = EventResourceAllocation.query.all()
            error = None  # Clear any previous errors, show success message
            flash("Resource allocated successfully!", "success")

    return render_template(
        'allocate.html',
        events=events,
        resources=resources,
        allocations=allocations,
        error=error
    )


@app.route('/allocations')

def view_allocations():
    # Redirect to unified allocate page
    return redirect(url_for('allocate_resource'))


@app.route('/allocations/remove/<int:alloc_id>', methods=['POST'])

def remove_allocation(alloc_id):
    allocation = EventResourceAllocation.query.get_or_404(alloc_id)
    event = Event.query.get(allocation.event_id)

    # get current user
    username = session.get('user')
    user = None
    if username:
        user = User.query.filter_by(username=username).first()

    # Only the event owner can remove allocation (no admin flag in User model)
    if event:
        # guard against missing `user_id` on Event model
        if hasattr(event, 'user_id'):
            event_owner_id = getattr(event, 'user_id')
            current_user_id = getattr(user, 'user_id', None) if user else None
            
            # Allow if admin or owner
            if (not user or user.username != 'admin') and (current_user_id is None or event_owner_id != current_user_id):
                flash('You are not authorized to remove this allocation.')
                return redirect(url_for('view_allocations'))

    try:
        db.session.delete(allocation)
        db.session.commit()
        flash('Allocation removed successfully!')
    except Exception as e:
        db.session.rollback()
        flash('Error removing allocation: ' + str(e))

    return redirect(url_for('view_allocations'))


# -------------------------------------------------
# Resource Utilization Report
# -------------------------------------------------
@app.route('/report', methods=['GET', 'POST'])

def utilization_report():
    report_data = []

    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()

        for resource in Resource.query.all():
            total_hours = bookings = upcoming = 0

            for alloc in resource.allocations:
                event = alloc.event
                event_date = event.start_time.date()

                if start_date <= event_date <= end_date:
                    total_hours += (event.end_time - event.start_time).total_seconds() / 3600
                    bookings += 1

                if event.start_time.date() > date.today():
                    upcoming += 1

            report_data.append({
                'name': resource.resource_name,
                'type': resource.resource_type,
                'hours': round(total_hours, 2),
                'bookings': bookings,
                'upcoming': upcoming
            })

    return render_template('report.html', report_data=report_data)


# -------------------------------------------------
# Admin User Management
# -------------------------------------------------

# -------------------------------------------------
# Run Application
# -------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
