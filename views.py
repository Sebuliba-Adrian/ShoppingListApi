"""

"""
from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from models import db, Category, CategorySchema, Item, ItemSchema
from sqlalchemy.exc import SQLAlchemyError
import status
from helpers import PaginationHelper
from flask_httpauth import HTTPBasicAuth
from flask import g
from models import User, UserSchema


auth = HTTPBasicAuth()


@auth.verify_password
def verify_user_password(name, password):
    user = User.query.filter_by(name=name).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


class AuthRequiredResource(Resource):
    method_decorators = [auth.login_required]


api_bp = Blueprint('api', __name__)
category_schema = CategorySchema()
item_schema = ItemSchema()
user_schema = UserSchema()
api = Api(api_bp)


class UserResource(AuthRequiredResource):
    def get(self, id):
        user = User.query.get_or_404(id)
        result = user_schema.dump(user).data
        return result


class UserListResource(Resource):
    @auth.login_required
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=User.query,
            resource_for_url='api.userlistresource',
            key_name='results',
            schema=user_schema)
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'user': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = user_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        name = request_dict['name']
        existing_user = User.query.filter_by(name=name).first()
        if existing_user is not None:
            response = {'user': 'An user with the same name already exists'}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            user = User(name=name)
            error_item, password_ok = \
                user.check_password_strength_and_hash_if_ok(
                    request_dict['password'])
            if password_ok:
                user.add(user)
                query = User.query.get(user.id)
                result = user_schema.dump(query).data
                return result, status.HTTP_201_CREATED
            else:
                return {"error": error_item}, status.HTTP_400_BAD_REQUEST
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST


class ItemResource(AuthRequiredResource):
    def get(self, id):
        item = Item.query.get_or_404(id)
        result = item_schema.dump(item).data
        return result

    def patch(self, id):
        item = Item.query.get_or_404(id)
        item_dict = request.get_json(force=True)
        if 'item' in item_dict:
            item_item = item_dict['item']
            if Item.is_unique(id=id, item=item_item):
                item.item = item_item
            else:
                response = {
                    'error': 'A item with the same item already exists'}
                return response, status.HTTP_400_BAD_REQUEST
        if 'duration' in item_dict:
            item.duration = item_dict['duration']
        if 'printed_times' in item_dict:
            item.printed_times = item_dict['printed_times']
        if 'printed_once' in item_dict:
            item.printed_once = item_dict['printed_once']
        dumped_item, dump_errors = item_schema.dump(item)
        if dump_errors:
            return dump_errors, status.HTTP_400_BAD_REQUEST
        validate_errors = item_schema.validate(dumped_item)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST
        try:
            item.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        item = Item.query.get_or_404(id)
        try:
            delete = item.delete(item)
            response = make_response()
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_401_UNAUTHORIZED


class ItemListResource(AuthRequiredResource):
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=Item.query,
            resource_for_url='api.itemlistresource',
            key_name='results',
            schema=item_schema)
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'item': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = item_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        item_item = request_dict['item']
        if not Item.is_unique(id=0, item=item_item):
            response = {
                'error': 'A item with the same item already exists'}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            category_name = request_dict['category']['name']
            category = Category.query.filter_by(name=category_name).first()
            if category is None:
                # Create a new Category
                category = Category(name=category_name)
                db.session.add(category)
            # Now that we are sure we have a category
            # create a new Item
            item = Item(
                item=item_item,
                duration=request_dict['duration'],
                category=category)
            item.add(item)
            query = Item.query.get(item.id)
            result = item_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST


class CategoryResource(AuthRequiredResource):
    def get(self, id):
        category = Category.query.get_or_404(id)
        result = category_schema.dump(category).data
        return result

    def patch(self, id):
        category = Category.query.get_or_404(id)
        category_dict = request.get_json()
        if not category_dict:
            resp = {'item': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = category_schema.validate(category_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            if 'name' in category_dict:
                category_name = category_dict['name']
                if Category.is_unique(id=id, name=category_name):
                    category.name = category_name
                else:
                    response = {
                        'error': 'A category with the same name already exists'}
                    return response, status.HTTP_400_BAD_REQUEST
            category.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        category = Category.query.get_or_404(id)
        try:
            category.delete(category)
            response = make_response()
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_401_UNAUTHORIZED


class CategoryListResource(AuthRequiredResource):
    def get(self):
        categories = Category.query.all()
        results = category_schema.dump(categories, many=True).data
        return results

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            resp = {'item': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = category_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        category_name = request_dict['name']
        if not Category.is_unique(id=0, name=category_name):
            response = {
                'error': 'A category with the same name already exists'}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            category = Category(category_name)
            category.add(category)
            query = Category.query.get(category.id)
            result = category_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST


api.add_resource(CategoryListResource, '/categories/')
api.add_resource(CategoryResource, '/categories/<int:id>')
api.add_resource(ItemListResource, '/items/')
api.add_resource(ItemResource, '/items/<int:id>')
api.add_resource(UserListResource, '/users/')
api.add_resource(UserResource, '/users/<int:id>')
