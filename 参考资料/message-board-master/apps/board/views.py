from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.views.decorators.csrf import requires_csrf_token
#from django.forms.models import model_to_dict

from datetime import datetime

from board.models import BoardForum, BoardTopic, BoardPost


def check_forum(request, forum):
    """
    Check if a forum exists and returns it if it does
    """
    exists = BoardForum.objects.filter(forum_id=forum).count() > 0
    if exists:
        return BoardForum.objects.get(forum_id=forum)
    elif forum is not None:
        return redirect('/board')
    else:
        return None


def check_topic(request, topic):
    """
    Check if a topic exists and return it if it does
    """
    if BoardTopic.objects.filter(topic_id=topic).count() > 0:
        return BoardTopic.objects.get(topic_id=topic)
    else:
        return redirect('/board')


def check_post(request, post):
    """
    Check if a post exists and return it if it does
    """
    if BoardPost.objects.filter(post_id=post).count() > 0:
        return BoardPost.objects.get(post_id=post)
    else:
        return redirect('/board')


def get_forum_path(request, current_forum):
    """
    Get the path to a forum from the board index
    """
    forum_path = []
    if current_forum:
        temp_forum = current_forum
        while temp_forum is not None:
            forum_path.append(temp_forum)
            temp_forum = getattr(temp_forum, 'forum_parent')
        return reversed(forum_path)
    else:
        return None


@requires_csrf_token
def board_forum(request, forum=None, page='1'):
    """
    This loads the sub-forums and topics for a specific forum
    """
    offset = (int(page) - 1) * 10
    msg = ''
    current_forum = check_forum(request, forum)
    forum_path = get_forum_path(request, current_forum)

    if request.method == 'POST' and (current_forum or forum is None):
        msg = board_try_add_forum(request, current_forum)
        board_try_add_topic(request, current_forum)

    forums = BoardForum.objects.filter(forum_parent=current_forum)
    topics = BoardTopic.objects.filter(topic_forum=current_forum) \
                       .order_by('-topic_pinned', 
                                 '-topic_pinned_date',
                                 '-topic_last_post__post_created_date')

    return render(request, 'board/forum.html',
                  {
                      'title': current_forum if current_forum else 'Board Index',
                      'current_forum': current_forum,
                      'forums': forums,
                      'topics': topics[offset : offset + 10],
                      'msg': msg if msg else '',
                      'is_staff': request.user.is_staff,
                      'is_logged_in': request.user.is_authenticated(),
                      'current_user': request.user,
                      'path': request.path,
                      'forum_path': forum_path,
                      'max_page': len(topics) / 10 + 1,
                      'pages': range(len(topics) / 10 + 1),
                      'current_page': int(page)
                  })


def board_try_add_forum(request, forum):
    """
    Adds a new forum if the current forum exists and the user has a staff account
    """
    if not (request.user.is_authenticated() and request.user.is_staff):
        return None
    forum_name = request.POST.get('forum-name', False)
    if forum_name:
        if forum is None:
            BoardForum.objects.get_or_create(forum_parent=None, forum_name=forum_name)
        else:
            if BoardForum.objects.filter(forum_parent=forum, forum_name=forum_name).count() > 0:
                return 'A forum with that name already exists'
            BoardForum.objects.get_or_create(forum_parent=forum, forum_name=forum_name)


@transaction.atomic
def board_try_add_topic(request, forum):
    """
    Adds a new topic if the user is logged in and the current forum exists
    """
    if not request.user.is_authenticated():
        return None
    topic_name = request.POST.get('topic-name', False)
    post_content = request.POST.get('post-content', False)
    if topic_name and post_content:
        topic = BoardTopic.objects.create(topic_forum=forum, 
                                          topic_creator=request.user, 
                                          topic_name=topic_name)
        post = BoardPost.objects.create(post_topic=topic, 
                                        post_creator=request.user, 
                                        post_content=post_content)
        setattr(topic, 'topic_last_post', post)
        topic.save()
        if forum:
            curr_topics = getattr(forum, 'forum_topic_count')
            setattr(forum, 'forum_topic_count', curr_topics + 1)
            curr_posts = getattr(forum, 'forum_post_count')
            setattr(forum, 'forum_post_count', curr_posts + 1)
            setattr(forum, 'forum_last_post', post)
            forum.save()


@requires_csrf_token
def board_topic(request, topic=None, page='1'):
    """
    Loads the page for a specific topic and all of the posts in it
    """
    offset = (int(page) - 1) * 10
    posts = None

    current_topic = check_topic(request, topic)
    forum = getattr(current_topic, 'topic_forum') if current_topic else None
    current_forum = check_forum(request, getattr(forum, 'forum_id')) if forum else None
    forum_path = get_forum_path(request, current_forum)

    if request.method == 'POST':
        board_try_add_post(request, current_forum, current_topic)
    elif current_topic:
        curr_views = getattr(current_topic, 'topic_view_count')
        setattr(current_topic, 'topic_view_count', curr_views + 1)
        current_topic.save()

    posts = BoardPost.objects.filter(post_topic=topic) \
                     .order_by('post_created_date')

    return render(request, 'board/topic.html',
                  {
                      'title': current_topic,
                      'current_forum': current_forum,
                      'current_topic': current_topic,
                      'posts': posts[offset : offset + 10],
                      'is_staff': request.user.is_staff,
                      'is_logged_in': request.user.is_authenticated(),
                      'current_user': request.user,
                      'path': request.path,
                      'forum_path': forum_path,
                      'max_page': len(posts) / 10 + 1,
                      'pages': range(len(posts) / 10 + 1),
                      'current_page': int(page)
                  })


def board_try_add_post(request, forum, topic):
    """
    Adds a post if the topic exists and the user is logged in
    """
    if not request.user.is_authenticated():
        return None

    post = None
    post_content = request.POST.get('post-content', False)
    if topic and post_content:
        post = BoardPost.objects.create(post_topic=topic, 
                                        post_creator=request.user, 
                                        post_content=post_content)
        setattr(topic, 'topic_last_post', post)
        curr_replies = getattr(topic, 'topic_reply_count')
        setattr(topic, 'topic_reply_count', curr_replies + 1)
        topic.save()
        if forum:
            curr_posts = getattr(forum, 'forum_post_count')
            setattr(forum, 'forum_post_count', curr_posts + 1)
            setattr(forum, 'forum_last_post', post)
            forum.save()
    return post


def board_post(request, post):
    """
    Renders a page for a specific post
    """
    current_post = check_post(request, post)
    return render(request, 'board/post.html', 
                  {
                      'ajax': False,
                      'post': current_post,
                      'is_logged_in': request.user.is_authenticated(),
                      'current_user': request.user
                  })


def board_post_edit(request, post):
    """
    Edits the post using variables passed in through a POST request
    Currently, this is only done through AJAX
    """
    current_post = check_post(request, post)
    if not request.user.is_authenticated():
        if request.method == 'GET':
            return redirect('/board/post/' + getattr(current_post, 'post_id'))
        else:
            msg = 'Not logged in'
    if not (getattr(current_post, 'post_creator') == request.user):
        return HttpResponse('Wrong user')
    if request.method == 'POST':
        new_content = request.POST.get('post-new-content', False)
        if new_content:
            setattr(current_post, 'post_content', new_content)
            setattr(current_post, 'post_edited_date', datetime.now())
            current_post.save()
            msg = 'Success'
    else:
        msg = 'Not changed'
    return render(request, 'board/post.html', 
                  {
                      'ajax': True,
                      'post': current_post,
                      'is_logged_in': request.user.is_authenticated(),
                      'current_user': request.user,
                      'msg': msg
                  })


def board_add_post_ajax(request, topic):
    """
    A function that allows adding posts using AJAX
    """
    if not request.user.is_authenticated():
        return None
    current_topic = check_topic(request, topic)
    forum = getattr(current_topic, 'topic_forum') if current_topic else None
    current_forum = check_forum(request, getattr(forum, 'forum_id')) if forum else None

    post = None
    if request.method == 'POST':
        post = board_try_add_post(request, current_forum, current_topic)
    else:
        return redirect('/board')

    return render(request, 'board/post.html', 
                  {
                      'ajax': True,
                      'post': post,
                      'is_logged_in': request.user.is_authenticated(),
                      'current_user': request.user
                  })


def board_pin_topic_ajax(request, topic):
    """
    Allows pinning topics using AJAX
    """
    if not (request.user.is_authenticated() and request.user.is_staff):
        return redirect('/board')

    current_topic = check_topic(request, topic)
    if current_topic:
        topic_pinned = getattr(current_topic, 'topic_pinned')
        if not topic_pinned:
            setattr(current_topic, 'topic_pinned_date', datetime.now())
        setattr(current_topic, 'topic_pinned', not topic_pinned)
        current_topic.save()
        return HttpResponse('Pin') if topic_pinned else HttpResponse('Unpin')
    else:
        return HttpResponse('Error')