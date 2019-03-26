import pytesseract
from PIL import Image
import textrazor

    
def Generate_Data(content, key):
    
    textrazor.api_key = key
    client = textrazor.TextRazor(extractors=["entities", "topics"])

    response = client.analyze(content)
    
    medicines = []
    person = []
    hospital = ""
    date = ""
    doctor = ""
    patient = ""
    
    for entity in response.entities():
        if 'ChemicalSubstance' in entity.dbpedia_types:        #Case when entity is recongnised as ChemicalSubstance
            medicines.append(entity.id)
        if 'Person' in entity.dbpedia_types:                   #Case when entity is recongnised as Person
            person.append(entity.id)
        if 'Company' in entity.dbpedia_types:                  #Case when entity is recongnised as Company
            hospital = entity.id        
        if 'Date' in entity.dbpedia_types:                     #Case when entity is recongnised as Date
            date = entity.id
    
    index = content.find(person[0])    #index of person 0 in string
    drindex = content.find(person[1])       #index of 'DR.' in string
    
    if index > drindex:                #If Dr. and person1 strings are nearby
        doctor = person[0]
        patient = person[1]
    else:                              #If Dr. and person0 are far away
        doctor = person[1]
        patient = person[0]
    
    print("This Bill is genreated by Hospital : "+hospital+"\nDated : " + date)
    print("Patient's Name:" + patient)
    print("Doctor's Name:" + doctor)
    print("Medicines:")
    for medicine in medicines:
        print(medicine)



"""
For Illustration purposes we have the below data, we won't include this data in out actual file
Key is confidential, take care not to push it on github :P 
:P :P :P :P
"""

content = """
                Apex Institute of Medical Sciences
        
                Date : 30/02/19
                
                Patient Details :
                Name : Rahul Kaushik Age : 30 yrs
                
                Rx
                
                Paracetamol (100mg)
                Alprazolam
                Amitriptyline
                Amlodipine
                Amoxicillin
                
                Doctor’s Name Doctor’s Signature
                
                Dr.Alexander Rahul
          """
key = "308ad87de7772313af92cd79514ce2d329112cdd7390c877f3406b6b"

Generate_Data(content, key)
    
