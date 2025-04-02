# Generated by Django 5.1.5 on 2025-04-02 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_site_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='button_2',
            field=models.CharField(blank=True, default='Перейти на 1WIN', null=True, verbose_name='Текст кнопки 2'),
        ),
        migrations.AlterField(
            model_name='site',
            name='description',
            field=models.TextField(blank=True, default='\n     <p> Используйте промокод: <a id="hero__promo" href="#">1winrupromo</a> и получите бонус <strong id="hero__price">до&nbsp;50&nbsp;000 рублей</strong> при регистрации.</p>\n    ', null=True, verbose_name='Текст куска заголовка'),
        ),
        migrations.AlterField(
            model_name='site',
            name='description_1',
            field=models.TextField(blank=True, default='\n    <p >\n                Чтобы войти на игровой портал БК достаточно иметь доступ в\n                интернет и мобильный телефон или ПК. Игрок должен открыть\n                официальный сайт и пройти простую регистрацию в несколько шагов.\n                Это займет не более 10-15 минут вашего времени.\n              </p>\n              <p  >\n                Вход в личный кабинет осуществляется через логин и пароль. Для\n                этого игроку достаточно использовать свой номер телефона или\n                email.\n              </p>\n              <p  >\n                Букмекерская контора принимает ставки на спорт, игры с живыми\n                дилерами и казино. Чтобы получить все преимущества, необходимо\n                зарегистрироваться на сайте букмекерской конторы.\n              </p>\n              <p  >\n                1win – идеальное online-casino для тех, кто любит различные\n                игровые развлечения. Игровые автоматы включают от простых слотов\n                до сложных игр казино. Здесь есть все для настоящих\n                профессионалов и новичков, чтобы с пользой провести игровые\n                развлечения.\n              </p>\n              <p  >\n                К каждой игре прилагаются четкие тексты описания и инструкции,\n                чтобы игрок смог как можно быстрее сосредоточиться на самом\n                главном – получении удовольствия!\n              </p>\n              <p  >\n                Благодаря приятным бонусам, предлагаемым на сайте БК, игроки\n                могут регулярно и бесплатно играть, приумножая свои средства.\n                Колесо фортуны, которое открывается после первого входа в\n                систему в течение дня, – это то, чего вы действительно ждете с\n                нетерпением. Просто вращайте его и получайте свои бонусы и\n                реальные деньги. Казино приготовило много специальных акций и\n                турниров, с которыми можно отдельно познакомиться на сайте. В\n                любое время игрок может зарегистрироваться и получить доступ к\n                захватывающему игровому миру.\n              </p>\n              <p  >\n                Все зеркала и альтернативные версии подключены к одной базе.\n                Если ограничен доступ на одной площадке, то вы можете свободно\n                зайти с другого сайта. Для доступа в учетную запись достаточно\n                вести логин и пароль, после чего свободно играть на деньги.\n              </p>\n              <p  >\n                Вы можете не только играть онлайн, но и скачать приложение на\n                android или iphone в свободном доступе. Благодаря установленной\n                программе на телефон игрок в любое время может делать ставки и\n                быть в игре.\n              </p>\n              <p  >\n                Компания Google блокирует приложения с азартными играми, поэтому\n                скачать программу на свое мобильное устройство вы можете через\n                рабочее зеркало официального сайта 1вин. Это бесплатно и\n                безопасно. Достаточно в поисковике найти подходящий сайт и зайти\n                на него по ссылке, где выбрать в меню «Скачать». Как только файл\n                загрузится, его можно сразу же устанавливать.\n              </p>\n    ', null=True, verbose_name='Текст 1'),
        ),
        migrations.AlterField(
            model_name='site',
            name='description_2',
            field=models.TextField(blank=True, default='\n     <p >\n                В Букмекерской конторе представлено огромное количество слотов и\n                игровых автоматов. Сотни наименований ждут своего часа, и многие\n                из них имеют бесплатные игры и захватывающие функции.\n              </p>\n              <p >\n                Зарегистрироваться на официальном сайте 1win могут все игроки в\n                режиме реального времени. Для этого достаточно зайти на\n                официальный сайт, заполнить краткую анкету и дождаться\n                подтверждения по смс или email.\n              </p>\n              <p >\n                Игроки должны помнить о том, что для того, чтобы успешно\n                зарегистрироваться на официальном сайте 1вин необходимо\n                указывать только реальные данные. Если введены фиктивные\n                сведения, то баланс будет заблокирован без возможности\n                восстановления.\n              </p>\n              <p >\n                Букмекерская контора предлагает игрокам два способа регистрации:\n              </p>\n            <ul >\n              <li>\n                через соцсети – осуществляется привязка к одному из аккаунтов\n                игрока (например, через mail.ru, steam, google);\n              </li>\n              <li>мгновенная регистрация по номеру телефона.</li>\n            </ul>\n            <p >\n              Важно отметить, что верификация – это не обязательная процедура.\n              БК может потребовать подтверждения в случае крупных выигрышей.\n              Администрация может запросить у клиента документ о подтверждении\n              личности.\n            </p>\n            <p >\n              Это не просто Букмекерская контора но и платформа для игр казино,\n              которая имеет современный геймплей. Игры букмекера отлично\n              смотрятся и воспроизводятся как на настольном компьютере с большим\n              экраном, так и на мобильном устройстве. Пользователи могут\n              наслаждаться превосходным качеством игр, которые добавят элемент\n              азарта в повседневную жизнь. Игровой процесс некоторых игр\n              адаптирован для маленьких экранов, например, с помощью специальных\n              кнопок и упрощенных пользовательских интерфейсов. Делать онлайн\n              ставки игроки могут в любое время суток, выбирая рабочее зеркало\n              официального сайта.\n            </p>\n            <p >\n              Игровая платформа, на которой можно зарабатывать или делать ставки\n              на реальные деньги. Игрок получает виртуальную валюту в виде\n              различных ежедневных бонусов, которые можно использовать для\n              ставок в слотах и играх. Также можно вносить депозит – он дает еще\n              больше преимуществ и возможностей.\n            </p>\n            <p >\n              Каждый реальный игрок может получить бонус зарегистрировавшись на\n              сайте 1вин. Приветственный фрибет начисляется тем клиентам,\n              которые следуют правилам букмекера.\n            </p>\n            <p >\n              Как только игрок зарегистрировался и внес минимальный депозит, на\n              его счет начисляется приятный бонус. Пользоваться такими\n              преимуществами могут только зарегистрированные игроки.\n            </p>\n            <p >\n              Каждый игрок может ощутить выгоду от регистрации, ведь получение\n              фрибета открывает массу игровых возможностей.\n            </p>\n    ', null=True, verbose_name='Текст 2'),
        ),
        migrations.AlterField(
            model_name='site',
            name='description_4',
            field=models.TextField(blank=True, default='\n    <p>\n                Букмекерская контора 1win – это международная компания,\n                доступная для игроков из разных уголков мира. Официальный сайт\n                дает массу преимуществ игрокам, начиная от получения\n                приветственного бонуса и заканчивая возможностью приумножения\n                крупных выигрышей.\n              </p>\n              <p>Преимущества казино:</p>\n            <ul>\n              <li>широкий выбор слотов и игр;</li>\n              <li>доступные бонусы для новичков и профессионалов;</li>\n              <li>удобный и мгновенный вывод денег;</li>\n              <li>доступ 24/7;</li>\n              <li>адаптивная и безопасная мобильная версия сайта;</li>\n              <li>интуитивно понятное управление;</li>\n              <li>зарегистрироваться в один клик;</li>\n              <li>\n                дизайн в сине-голубых оттенках способствует концентрации\n                внимания;\n              </li>\n              <li>лицензионная компания.</li>\n            </ul>\n              <p>\n                Чтобы зайти на сайт игроки могут использовать зеркало, которое\n                помогает избежать множества блокировок.\n              </p>\n              <p>\n                На каждом игровом уровне предусмотрены фриспины, которые\n                начисляются в разном процентном соотношении. Зарегистрированый\n                пользователь может получить бездепозитный бонус (он стает\n                доступным после внесения депозита).\n              </p>\n              <p>\n                Все бонусы и награды игроку зачисляются автоматически на счет.\n                Без строгих ограничений он может выводить деньги на карту при\n                наличии подтвержденного аккаунта. Прокручивать слоты гости сайта\n                могут при внесении минимального депозита, открывая для себя\n                множество игровых возможностей\n              </p>\n              <p>\n                Также действует постоянная бонусная программа для опытных\n                игроков. Акциями и промокодами можно пользоваться сразу же после\n                регистрации. Каждый промокод используют только один раз, поэтому\n                будьте внимательными, чтобы не упустить возможность удвоить свой\n                выигрыш.\n              </p>\n              <p>\n                Играть в казино можно без ограничений во времени. Если вы хотите\n                быть активным игроком в любое время, тогда поспешите скачать\n                приложение в свободном доступе.\n              </p>\n              <p>\n                Зарегистрироваться на сайте 1ВИН могут только совершеннолетние\n                лица. Получать первые выигрыши можно без прохождения\n                верификации, но в случае срывания крупных ставок администрация\n                БК требует пройти верификацию (игроку достаточно загрузить сканы\n                документов для подтверждения своей личности).\n              </p>\n              <p>\n                Все игровые автоматы адаптированы для работы на мобильных\n                устройствах, поэтому имеют упрощенный интерфейс. Можно играть и\n                онлайн, выбрав переход по альтернативной ссылке.\n              </p>\n              <p>\n                Ежедневно казино от БК радостно приветствует новых игроков,\n                которые имеют шанс воспользоваться подарочными комбинациями\n                после создания личного кабинета.\n              </p>\n    ', null=True, verbose_name='Текст 4'),
        ),
        migrations.AlterField(
            model_name='site',
            name='description_5',
            field=models.TextField(blank=True, default='\n    <p>\n                1вин – всемирно известная букмекерская контора, которая\n                пользуется популярностью среди опытных игроков и новичков.\n                Букмекерская контора заинтересована в привлечении новых\n                пользователей и поэтому предлагает не только выгодные\n                приветственные бонусы, но и уникальные промокоды. Все эти\n                преимущества доступны только зарегистрированным пользователям.\n                Зарегистрироваться на сайте можно в несколько кликов.\n              </p>\n              <p>\n                Первый бонус, который может получить игрок после регистрации на\n                сайте, – это приветственный. Ввести промокод необходимо в\n                специальном поле регистрационной анкеты. Перед тем, как нажать\n                кнопку подтверждения следует проверить все данные, иначе при\n                допущении ошибки уникальный код больше не будет действовать. На\n                депозит начисляется +200%. Умноженные средства можно\n                использовать для реальных игр на деньги.\n              </p>\n              <p>\n                Однако без депозита приветственный бонус не будет начислен. При\n                выполнении этого обязательного условия перед игроком открывается\n                масса возможностей.\n              </p>\n              <p>\n                Зарегистрированные игроки могут периодически участвовать в\n                акциях и получать уникальные коды, которые компания присылает в\n                виде ссылки на электронную почту. После перехода по ссылке и\n                входа в аккаунт пользователь может использовать все\n                предоставленные преимущества.\n              </p>\n              <p>\n                Игрок должен знать, где вводить промокод, чтобы не упустить свой\n                шанс удвоения выигрыша. Приветственный код вводится в поле\n                анкеты, после чего начисляются дополнительные средства на счет\n                пользователя. Проверить их количество игрок может в своем\n                аккаунте, который легко открыть как в браузере, так и в\n                мобильном приложении.\n              </p>\n              <p>\n                Все новые промокоды можно активировать, если ввести их в поле\n                «Добавить промокод». Как только уникальный код внесен, система\n                сразу отображает изменения на игровом счету.\n              </p>\n              <p>\n                Каждый ваучер прибавляет сумму выигрыша в разном количестве –\n                это зависит от правил компании и действующих условий.\n              </p>\n              <p>\n                Действуют на сегодня и другие промокоды компании, которые можно\n                найти в разных социальных сетях. Например, игрок, вступивший в\n                группу Вконтакте или подписавшись на телеграм-сообщество, будет\n                всегда в курсе событий.\n              </p>\n              <p>\n                В 2022 году БК при пополнении игрового счета поощрила сотни\n                пользователей. Стоит помнить, что каждый предоставленный\n                промокод является одноразовым.\n              </p>\n              <p>\n                Регистрируйтесь в казино 1вин и получайте вознаграждения по\n                промокоду, который позволяет увеличить процентную ставку на\n                100-200 %.\n              </p>\n    ', null=True, verbose_name='Текст 5'),
        ),
        migrations.AlterField(
            model_name='site',
            name='name_of_site',
            field=models.CharField(blank=True, null=True, verbose_name='Название сайта'),
        ),
        migrations.AlterField(
            model_name='site',
            name='title',
            field=models.CharField(blank=True, default='\n    1WIN ВХОД НА&nbsp;ОФИЦИАЛЬНЫЙ САЙТ\n    ', null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='title_1',
            field=models.CharField(blank=True, default='\n     О компании\n    ', null=True, verbose_name='Заголовок 1'),
        ),
        migrations.AlterField(
            model_name='site',
            name='title_2',
            field=models.CharField(blank=True, default='1 WIN регистрация', null=True, verbose_name='Заголовок 2'),
        ),
        migrations.AlterField(
            model_name='site',
            name='title_3',
            field=models.CharField(blank=True, default='1 WIN зеркало', null=True, verbose_name='Заголовок 3'),
        ),
        migrations.AlterField(
            model_name='site',
            name='title_4',
            field=models.CharField(blank=True, default='Заголовок 4', null=True, verbose_name='Заголовок 4'),
        ),
        migrations.AlterField(
            model_name='site',
            name='title_5',
            field=models.CharField(blank=True, default='Заголовок 5', null=True, verbose_name='Заголовок 5'),
        ),
    ]
