from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import View

from minesweeper.constants import WON, LOST
from minesweeper.models import MinesweeperGame


class AjaxResetGame(JSONResponseMixin, AjaxResponseMixin, View):
    """ Resets the game for the provided ID
    """

    def get_ajax(self, request, *args, **kwargs):
        context = {}
        # Get our Dossier Object
        game_id = request.GET.get('game_id', None)

        try:
            game = MinesweeperGame.objects.get(id=game_id)
        except MinesweeperGame.DoesNotExist:
            game = None

        if game:
            game.start()
            json_boardstate = game.client_json_boardstate()
            context['json_boardstate'] = json_boardstate
            context['game_status'] = game.status
        else:
            context['message'] = 'Game with ID {} not found'.format(game_id)
            context['message_class'] = 'alert alert-danger'

        return self.render_json_response(context)


class AjaxProcessMove(JSONResponseMixin, AjaxResponseMixin, View):
    """ Accepts a User move, processes it and returns the updated boardstate.
    """

    def get_ajax(self, request, *args, **kwargs):
        context = {}
        # Get our Dossier Object
        game_id = request.GET.get('game_id', None)
        move_type = request.GET.get('move_type', 'clear')
        x = request.GET.get('x', None)
        y = request.GET.get('y', None)

        try:
            game = MinesweeperGame.objects.get(id=game_id)
        except MinesweeperGame.DoesNotExist:
            game = None

        if game and x and y:
            game.user_move(int(x), int(y), move_type)
            json_boardstate = game.client_json_boardstate()
            context['json_boardstate'] = json_boardstate
            if game.status == WON:
                context['message'] = 'You win!  Hit Reset to play again.'
            elif game.status == LOST:
                context['message'] = 'You Lost!  Hit Reset to try again.'
            context['game_status'] = game.status
        else:
            context['message'] = 'Game with ID {} not found'.format(game_id)

        return self.render_json_response(context)
