from news_lk3.custom_newspapers import (AdaDeranaLk, AdaDeranaSinhalaLk, AdaLk,
                                        BBCComSinhala, CeylonTodayLk,
                                        ColomboTelegraphCom, DailyFtLk,
                                        DailyMirrorLk, DailyNewsLk,
                                        DBSJeyarajCom, DivainaLk,
                                        EconomyNextCom, IslandLk, LankadeepaLk,
                                        NewsFirstLk, TamilMirrorLk,
                                        VirakesariLk)


class NewspaperFactory:
    @staticmethod
    def list_all():
        return [
            AdaDeranaLk,
            AdaDeranaSinhalaLk,
            AdaLk,
            BBCComSinhala,
            CeylonTodayLk,
            ColomboTelegraphCom,
            DailyFtLk,
            DailyMirrorLk,
            DailyNewsLk,
            DBSJeyarajCom,
            DivainaLk,
            EconomyNextCom,
            IslandLk,
            LankadeepaLk,
            NewsFirstLk,
            TamilMirrorLk,
            VirakesariLk,
        ]

    @staticmethod
    def list_all_testing():
        return [
            CeylonTodayLk,
        ]
