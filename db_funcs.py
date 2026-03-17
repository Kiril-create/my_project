    all_games = Game.query.all()
    return all_games


def get_all_users() -> list[User]:
    all_users = User.query.all()
    return all_users


def save_data(update: Update, context: CallbackContext) -> int:
    user = check_user(context.user_data['telegram_id'])
    user = False  # удалить
    if not user:
        new_user = User(
            telegram_id=context.user_data['telegram_id'],
            full_name=context.user_data['user_name'],
            wishlist=context.user_data['wishlist'],
            region=context.user_data['region'],
        )
        db_session.add(new_user)
        db_session.commit()
        user_id = new_user.id
        return user_id
    return False


def update_games(shop: str, games_from_shop: dict[str, str | float]) -> None:
    all_games_from_wishlists = get_all_games()
    titles_from_wishlists = [game.title for game in all_games_from_wishlists]
    ids_from_wishlists = [game.id for game in all_games_from_wishlists]
    for game_card in games_from_shop:
        if game_card['title'] in titles_from_wishlists:
            title_index = titles_from_wishlists.index(game_card['title'])
            game_id = ids_from_wishlists[title_index]
            game = Game.query.get(game_id)
            setattr(game, f'{shop}_actual_price', game_card['actual_price'])
            setattr(game, f'{shop}_url', game_card['url'])
            db_session.commit()


# int float bool
# list[int] list[str]
# (vasya, 20, moscow) tuple[str, int, str]
# set[int] set[str]
# dict[str, int]
