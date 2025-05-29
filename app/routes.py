from fastapi import Path, HTTPException, Query
from fastapi.responses import JSONResponse
from models import Patient, PatientUpdate
from crud import load_data, save_data

def define_routes(app):
    #first endpoint
    @app.get('/')
    def hello():
        return {'message' : 'Patient Management System API'}

    #second endpoint
    @app.get('/about')
    def about():
        return {'message':'A fully functional API to manage your patient records'}

    @app.get('/view')
    def view():
        data = load_data()
        return data

    #Endpoint using path parameter
    @app.get('/patient/{patient_id}')
    def view_patient(patient_id: str = Path(..., description='ID of the patient in DB', example='p001')):
        #load all the patient
        data = load_data()
        if patient_id.upper() in data:
            return data[patient_id.upper()]
        raise HTTPException(status_code=404, detail='Patient not found')

    #Endpoint using query parameter
    @app.get('/sort')
    def sort_patients(sort_by: str = Query(..., description ='sort on the basis of height , weight or bmi '), order: str = Query('asc', description='sort in ascending or descending order')):
        valid_fields = ['height', 'weight', 'bmi']
        if sort_by not in valid_fields:
            raise HTTPException(status_code=400, detail=f'Invalid field! Select from {valid_fields}')
        if order not in ['asc', 'desc']:
            raise HTTPException(status_code=400, detail='Invalid order! select between asc and desc')
        
        data = load_data()
        sort_order = True if order == 'desc' else False
        sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
        return sorted_data

    @app.post('/create')
    def create_patient(patient: Patient):
        #load exisiting data
        data = load_data()
        #To check if patient already exist
        if patient.id.upper() in data.keys():
            raise HTTPException(status_code=400, detail='Patient already exists.')
        
        #new patient added to database
        data[patient.id.upper()] = patient.model_dump(exclude='id')
        #save into json file
        save_data(data)
        return JSONResponse(status_code=201, content='Patient created successfully')

    #update end-point
    @app.put('/edit/{patient_id}')
    def update_patient(patient_id: str, patient_update: PatientUpdate):
        updated_patient_id = patient_id.upper()
        
        data = load_data()
        if updated_patient_id not in data:
            raise HTTPException(status_code=404, detail='patient not found')

        existing_patient_info = data[updated_patient_id]
        updated_info = patient_update.model_dump(exclude_unset=True) #only updated data by client will be included, not the default one.

        for key, value in updated_info.items(): #loop on updated, but change on existed...
            existing_patient_info[key] = value

        #create object of Patient, coz- computed field needs to be calculate
        existing_patient_info['id'] = updated_patient_id
        patient_pydantic_object = Patient(**existing_patient_info)
        #back to dictionary excluding id
        existing_patient_info = patient_pydantic_object.model_dump(exclude='id')
        #add this dictionary to data
        data[updated_patient_id] = existing_patient_info
        #save data
        save_data(data)
        return JSONResponse(status_code=200, content={'message': 'updated'})

    @app.delete('/delete/{patient_id}')
    def delete_patient(patient_id: str):
        #load data
        data = load_data()
        
        if patient_id.upper() not in data:
            raise HTTPException(status_code=400, detail='Patient id not found')
        
        del data[patient_id.upper()]
        save_data(data)
        return JSONResponse(status_code=204, content='"message": "Patient deleted"')