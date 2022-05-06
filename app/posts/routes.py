from flask import Blueprint
from posts.controller import create_post, get_posts

post_bp = Blueprint('post_bp', __name__)

post_bp.route('/posts', methods=['GET'], defaults={"page": 1})(get_posts) 
post_bp.route("/posts/<int:page>", methods=["GET"])(get_posts)
post_bp.route("/post/create", methods=["POST"])(create_post)