# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db import IntegrityError
import os
from django.shortcuts import redirect
from django.views import generic
from django.core.paginator import Paginator
from .models import Board, Section, Pin

def showcase(request, section_slug):
    section_list = Section.objects.filter(active=True)
    section = section_list.get(slug=section_slug)
    section_list = section_list.exclude(slug=section_slug)
    section_id = int(section.id_pinterest)
    pins = Pin.objects.filter(section__id_pinterest=section_id)
    paginator = Paginator(pins, 15)
    page = request.GET.get('page')
    pins = paginator.get_page(page)
    paginate_limit = [3, -3]
    title_custom_split = section.title.replace('[ ', '').split(' ] ')
    slug_custom_split = section.title.replace('[ ', '').split(' ] ')[0].replace(' ', '-').lower()
    menu_description = '{} {} {}'.format('Artworks by', title_custom_split[0], 'on')
    return render(request, 'gallery/showcase.html', {
        'section_list': section_list,
        'pins': pins,
        'section_title': title_custom_split,
        'section_slug': slug_custom_split,
        'menu_description': menu_description,
        'paginate_limit': paginate_limit
    })


class section_list(generic.ListView):
    model = Section
    queryset = Section.objects.filter(active=True)
    context_object_name = 'section_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        count = context['section_list'].count()
        # Add in a QuerySet of all the books
        context['menu_description'] = '{} {} {}'.format('There is', count, 'personal art galleries on')
        return context


def create_boards(request):
    # TODO remove hardcoded credential
    from pinlery.init_api import Pinterest
    pinterest = Pinterest(username='nennertrennen')
    boards = pinterest.get_user_boards()
    while boards:
        for board in boards:
            target_board_id = int(board['id'])
            new_board = Board(title=board['name'], id_pinterest=target_board_id)
            try:
                new_board.save()
            except IntegrityError:
                continue
        boards = pinterest.get_user_boards()

def create_sections(request):
    from pinlery.init_api import Pinterest
    pinterest = Pinterest()
    active_boards = Board.objects.filter(active=True)
    for board in active_boards:
        target_board_id = str(int(board.id_pinterest))
        sections = pinterest.get_board_sections(board_id=target_board_id)
        while sections:
            for section in sections:
                section_id = int(section['id'])
                new_section = Section(title=section['title'], id_pinterest=section_id, board=board, slug=section["slug"])
                try:
                    new_section.save()
                except IntegrityError:
                    continue
            sections = pinterest.get_board_sections(board_id=target_board_id, reset_bookmark=True)


def create_pins(request):
    from pinlery.init_api import Pinterest
    pinterest = Pinterest()
    active_sections = Section.objects.filter(active=True, board__active=True)
    for section in active_sections:
        target_section_id = str(int(section.id_pinterest))
        pins = pinterest.get_section_pins(section_id=target_section_id)
        counter = 0
        while pins:
            for pin in pins:
                if len(pin["title"]) < 2 and len(pin["description"]) < 2:
                    pin_title = "Untitled"
                elif len(pin["title"]) < 2:
                    pin_title = pin["description"][0:27]
                else:
                    pin_title = pin["title"]
                pin_id = int(pin['id'])
                new_pin = Pin(id_pinterest=pin_id, title=pin_title, section=section,
                              image_url=pin["images"]["orig"]["url"],
                              width=pin["images"]["orig"]["width"],
                              height=pin["images"]["orig"]["height"],
                              small_image_url=pin["images"]["236x"]["url"],
                              width_s=pin["images"]["236x"]["width"],
                              height_s=pin["images"]["236x"]["height"],
                              medium_image_url=pin["images"]["736x"]["url"],
                              width_m=pin["images"]["736x"]["width"],
                              height_m=pin["images"]["736x"]["height"],
                              color=pin['dominant_color'],
                              sort_position=counter)
                counter += 1
                try:
                    new_pin.save()
                except IntegrityError:
                    counter += 1
                    continue
            pins = pinterest.get_section_pins(section_id=target_section_id, reset_bookmark=True)