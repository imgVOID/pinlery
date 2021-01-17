# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
import os
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import Board, Section, Pin, Profile


class pin_list(ListView):
    model = Pin
    template_name = "gallery/pages/showcase.html"
    active_sections = Section.objects.filter(active=True)
    context_object_name = 'pins'
    paginate_by = 9

    def get_queryset(self):
        self.section = get_object_or_404(Section, slug=self.kwargs.get("section_slug"))
        pins = Pin.objects.filter(section=self.section)
        self.pins_count = Pin.objects.filter(section=self.section).count()
        return pins

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_description'] = '{} {} {}'.format('About', self.pins_count, 'items')
        context['active_sections'] = self.active_sections.exclude(slug=self.section.slug)
        context['paginate_limit'] = [3, -3]
        context['section'] = self.section
        return context


class section_list(ListView):
    model = Section
    queryset = Section.objects.filter(active=True)
    context_object_name = 'section_list'
    template_name = "gallery/pages/section_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        count = context['section_list'].count()
        context['menu_description'] = '{} {} {}'.format('There is', count, 'personal art galleries on')
        return context


def create_boards(request):
    from pinlery.init_api import Pinterest
    active_users = Profile.objects.filter(active=True)
    for user in active_users:
        pinterest = Pinterest(username=user.username)
        boards = pinterest.get_user_boards()
        while boards:
            for board in boards:
                target_board_id = int(board['id'])
                new_board = Board(title=board['name'],
                                  user=user,
                                  id_pinterest=target_board_id)
                try:
                    new_board.save()
                except IntegrityError:
                    continue
            boards = pinterest.get_user_boards()
    return redirect('/admin/gallery/board')


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

    return redirect('/admin/gallery/section')


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
                pin_id = int(pin['id'])
                new_pin = Pin(id_pinterest=pin_id, title=pin["title"],
                              description=pin["description"], section=section,
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

    return redirect('/admin/gallery/pin')
