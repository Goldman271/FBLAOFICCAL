from flet import *


def sync_board_destinations(self):
    boards = self.store.get_boards()
    self.bottom_nav_rail.destinations = []
    for i in range(len(boards)):
        b = boards[i]
        self.bottom_nav_rail.destinations.append(
            NavigationRailDestination(
                label_content=TextField(
                    value=b.name,
                    hint_text=b.name,
                    text_size=12,
                    read_only=True,
                    on_focus=self.board_name_focus,
                    on_blur=self.board_name_blur,
                    border="none",
                    height=50,
                    width=150,
                    text_align="start",
                    data=i
                ),
                label=b.name,
                selected_icon=icons.CHEVRON_RIGHT_ROUNDED,
                icon=icons.CHEVRON_RIGHT_OUTLINED
            )
        )
    self.view.update()

