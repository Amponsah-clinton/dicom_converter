import io
import pydicom
from pydicom.dataset import Dataset, FileMetaDataset
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render

def convert_to_dicom(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']

        image = Image.open(image_file)

        if image.mode != 'L':
            image = image.convert('L')

        ds = Dataset()

        ds.PatientName = "Anonymous"
        ds.PatientID = "123456"
        ds.Modality = "OT" 
        ds.SOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
        ds.SOPInstanceUID = pydicom.uid.generate_uid()

        ds.Rows, ds.Columns = image.size
        ds.BitsAllocated = 8  
        ds.BitsStored = 8
        ds.HighBit = 7
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.PixelData = image.tobytes()

        file_meta = FileMetaDataset()
        file_meta.MediaStorageSOPClassUID = ds.SOPClassUID
        file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
        file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

        ds.file_meta = file_meta

        dicom_bytes = io.BytesIO()
        pydicom.dcmwrite(dicom_bytes, ds)

        dicom_bytes.seek(0)
        response = HttpResponse(dicom_bytes, content_type='application/dicom')
        response['Content-Disposition'] = 'attachment; filename="converted.dcm"'
        return response

    return render(request, 'upload.html')
