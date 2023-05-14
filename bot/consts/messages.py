"""Модуль сообщений."""
LINE = '\n——————————————————\n'
INPUT_FORMAT = 'ℹ️ Формат ввода: <b>{}</b>'

FLOAT_FORMAT = '123,123 или 123.123 или 123'

START_TEXT = 'Добро пожаловать в <b>ArbiBot</b> - бот для поиска арбитражных ситуаций.'

START_TITLE = '🏦 <b>ОСНОВНОЕ МЕНЮ</b>'

SETTINGS_TITLE = '⚙️ <b>НАСТРОЙКИ</b>'
SETTINGS_INFO = 'Расчетная монета: <b>{base_coin_name}</b>\n' \
                'Объем торгов: <b>{volume}</b>\n' \
                'Порог: <b>{threshold}</b>'
SETTINGS_BASE_COIN = 'Выберите новую расчетную монету'
SETTINGS_VOLUME = 'Введите новый объем торгов'
SETTINGS_THRESHOLD = 'Введите новый порог'

BUNDLES_TITLE = '🔄 <b>СВЯЗКИ</b>'
BUNDLES_EMPTY = 'Ваш список связок пуст'
BUNDLES_COIN = 'Выберите монету для новой отслеживаемой связки'
BUNDLES_EXCHANGE = 'Выберите необходимые биржи для <b>{}</b>'
BUNDLES_DELETE_BUNDLE = 'Выберите связку для удаления'

ARBI_EVENTS_TITLE = '🔄 <b>АРБИТРАЖНЫЕ СИТУАЦИИ</b>'
ARBI_EVENTS_EMPTY = 'Список пуст'

UNLINK_SUCCESS = 'Вы успешно отвязали свой telegram.'
ALREADY_UNLINKED = 'Ваш telegram не был привязан.'

NEW_EVENT_NOTIFICATION = '🆕 <b>НОВАЯ АРБИТРАЖНАЯ СИТУАЦИЯ</b>\n' \
                         '{line}' \
                         '<b>{ticker} / {bace_coin_ticker}</b>\n' \
                         '<b>{exchange1_name}</b> (<b>{first_price:.4f}</b>) ' \
                         '{direction} ' \
                         '<b>{exchange2_name}</b> (<b>{second_price:.4f}</b>)\n' \
                         '<b>Профит:</b> <b>{profit:.2f}</b>'
