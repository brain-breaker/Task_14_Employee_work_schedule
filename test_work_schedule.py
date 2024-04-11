from datetime import date, timedelta
from atf import log, info
from atf.ui import *
from pages.auth_page import AuthPage
from pages.work_schedule_documents import WorkScheduleDocuments


class TestWorkScheduleDocuments(TestCaseUI):

    @classmethod
    def setUpClass(cls):
        cls.browser.open(cls.config.get('SITE'))
        AuthPage(cls.driver).auth(cls.config.get('USER_LOGIN'), cls.config.get('USER_PASSWORD'))

    def setUp(self):
        WorkScheduleDocuments(self.driver).open_ews_documents()

    def test_01_checking_timeoff(self):
        """ Создать отгул
            Выбрать сотрудника через автодополнение, которому создаем отгул
            Выставить дату - завтра
            Заполнить причину
            Запустить в ДО
            Убедиться, что появился в реестре и при переоткрытии значения в полях сохранились
            Удалить отгул"""

        current_date = date.today()
        tomorrow_date = (current_date + timedelta(days=1)).strftime('%d.%m.%y')
        timeoff_data = {'Сотрудник': 'Задач Автотест',
                        'Причина': 'Хочу порешать задачи из курса по автотестированию'}

        timeoff_page = WorkScheduleDocuments(self.driver)
        log('Создаем отгул')
        timeoff_card = timeoff_page.create_document('Отгул', 'Отгул (для тестов мобилки)')
        log('Заполняем необходимые данные в отгуле')
        timeoff_card.fill_timeoff(**timeoff_data)
        timeoff_card.select_date(tomorrow_date)
        log('Запускаем отгул в ДО')
        timeoff_card.run_timeoff()
        info('Закрываем карточку отгула после запуска в ДО')
        timeoff_card.close()
        log('Находим наш отгул')
        timeoff_page.search_document(*timeoff_data.values())
        log('Открываем отгул')
        timeoff_page.open_document(timeoff_data['Причина'])
        log('Проверяем отгул')
        timeoff_card.check_timeoff(*timeoff_data.values(), tomorrow_date)
        log('Удаляем отгул')
        timeoff_card.delete_timeoff()
