from django.db import models

class Diabetespatientdata(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    pregnancies = models.FloatField()
    glucose = models.FloatField()
    blood_pressure = models.FloatField()
    skin_thickness = models.FloatField()
    insulin = models.FloatField()
    bmi = models.FloatField()
    diabetes_pedigree_function = models.FloatField()
    age = models.IntegerField()
    modelprediction = models.CharField(max_length=50)
    doctorverdict = models.CharField(max_length=255, blank=True, null=True)




class heartformdata(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    age =  models.IntegerField()
    sex = models.CharField(max_length=50)
    cp = models.FloatField()
    trestbps = models.FloatField()
    chol = models.FloatField()
    fbs = models.FloatField()
    restecg = models.FloatField()
    thalach = models.FloatField()
    exang = models.IntegerField()
    oldpeak = models.FloatField()
    slope = models.IntegerField()
    ca = models.IntegerField()
    thal = models.IntegerField()
    modelprediction = models.CharField(max_length=50)
    doctorverdict = models.CharField(max_length=255, blank=True)


class parkinsonformdata(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    MDVP_Fo_Hz = models.FloatField()
    MDVP_Fhi_Hz = models.FloatField()
    MDVP_Flo_Hz = models.FloatField()
    MDVP_Jitter_percent = models.FloatField()
    MDVP_Jitter_Abs = models.FloatField()
    MDVP_RAP = models.FloatField()
    MDVP_PPQ = models.FloatField()
    Jitter_DDP = models.FloatField()
    MDVP_Shimmer = models.FloatField()
    MDVP_Shimmer_dB = models.CharField(max_length=50)
    Shimmer_APQ3 = models.FloatField()
    Shimmer_APQ5 =models.FloatField()
    MDVP_APQ = models.FloatField()
    Shimmer_DDA = models.CharField(max_length=50)
    NHR = models.CharField(max_length=50)
    HNR = models.CharField(max_length=50)
    RPDE = models.CharField(max_length=50)
    DFA = models.CharField(max_length=50)
    spread1 = models.CharField(max_length=50)
    spread2 = models.CharField(max_length=50)
    D2 = models.CharField(max_length=50)
    PPE = models.CharField(max_length=50)
    modelprediction = models.CharField(max_length=50)
    doctorverdict = models.CharField(max_length=255, blank=True, null=True)


  
