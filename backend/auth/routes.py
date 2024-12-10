from flask import Blueprint, request, jsonify
from models import db, User




auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Пропущены поля'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'Пользователь уже существует'}), 400

    try:
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Регистрация успешна!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Пропущены поля'}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return jsonify({'message': 'Авторизация успешна!', 'email': user.email}), 200
    return jsonify({'error': 'Неверный email или пароль'}), 401


@auth_blueprint.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'hpsw': user.hpsw,
        'is_admin': user.is_admin,
        'time': user.time,
    } for user in users])


@auth_blueprint.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin') #Реализацию назначения админа надо будет обсудить

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    if username:
        user.username = username
    if email:
        if User.query.filter(User.email == email, User.id != user_id).first():
            return jsonify({'error': 'Email уже используется'}), 400
        user.email = email
    if password:
        user.set_password(password)
    if is_admin is not None: #Возможно проверку на None надо будет сделать со всеми полями (я не тестил)
        user.is_admin = is_admin

    try:
        db.session.commit()
        return jsonify({'message': 'Данные пользователя успешно обновлены'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_blueprint.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Пользователь удален'}), 200
    return jsonify({'error': 'Пользователь не найден'}), 404