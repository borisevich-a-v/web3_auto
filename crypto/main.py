from runner import Runner

db = ...  # initdatabase(settings)
queue = ...  #  initqueue(settings.worker_queue_name)

runner = Runner(db=db, queue=queue)
runner.run()
