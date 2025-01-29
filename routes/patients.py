



async def get_patietn(request: PatientRequestModel, db:AsyncSession = Depend(get_db)):
    respinse = tst(request, get_db)