"""Модуль сообщений."""
LINE = '\n——————————————————\n'
INPUT_FORMAT = 'ℹ️ Формат ввода: <b>{}</b>'

FLOAT_FORMAT = '123,123 или 123.123 или 123'

START_TEXT = 'Добро пожаловать в <b>ArbiBot</b> - бот для поиска арбитражных ситуаций.'
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

UNLINK_SUCCESS = 'Вы успешно отвязали свой telegram.'
ALREADY_UNLINKED = 'Ваш telegram не был привязан.'
