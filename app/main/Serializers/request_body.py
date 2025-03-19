from rest_framework import serializers

class ShablonName(serializers.Serializer):
    shablon_name=serializers.CharField()


class ChangeSite(serializers.Serializer):
    shablon_name = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    title_button = serializers.CharField()
    link_for_site = serializers.CharField()
    title_1 = serializers.CharField()
    description_1 = serializers.CharField()
    button_1 = serializers.CharField()
    link_for_site_1 = serializers.CharField()
    photo_1 = serializers.ImageField()
    title_2 = serializers.CharField()
    description_2 = serializers.CharField()
    photo_about_2 = serializers.ImageField()
    button_2 = serializers.CharField()
    link_for_site_2 = serializers.CharField()
    title_3 = serializers.CharField()
    description_3 = serializers.CharField()
    photo_about_3 = serializers.ImageField()
    button_3 = serializers.CharField()
    link_for_site_3 = serializers.CharField()
    title_4 = serializers.CharField()
    description_4 = serializers.CharField()
    title_5 = serializers.CharField()
    description_5 = serializers.CharField()

    # Основная инфа
    domain_name = serializers.CharField()
    name_of_site = serializers.CharField()
    main_link = serializers.CharField()
    yandex_metrika = serializers.ImageField()

    # Конфигурация сайта
    id_vebmaster = serializers.IntegerField()
    valuable_main_domain = serializers.CharField()
    promo_code = serializers.IntegerField()