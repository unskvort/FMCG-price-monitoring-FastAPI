from parser.updater import Updater

from apscheduler.schedulers.background import BackgroundScheduler


def updater_store() -> None:
    updater = Updater()
    updater.run()


scheduler = BackgroundScheduler()

scheduler.add_job(updater_store, "interval", days=1)
