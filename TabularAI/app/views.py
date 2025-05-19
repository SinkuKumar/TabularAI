# app/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .forms import UploadFileForm
import pandas as pd
from django.shortcuts import render

# Global variable to store dataframe (use session or cache for multi-user)
dataframe = None

def file_upload_view(request):
    global dataframe
    df = None
    if request.method == 'POST' and request.FILES.get('file'):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            filepath = uploaded_file.file.path
            if filepath.endswith('.csv'):
                df = pd.read_csv(filepath)
                dataframe = df
    else:
        form = UploadFileForm()
    
    return render(request, 'app/upload.html', {
        'form': form,
        'data': dataframe.to_html(classes="table table-bordered") if dataframe is not None else None
    })

@csrf_exempt
def ask_question(request):
    global dataframe
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question')

        if dataframe is not None:
            # TODO: Add LLM backend
            if 'average' in question.lower():
                answer = dataframe.mean(numeric_only=True).to_string()
            elif 'column' in question.lower():
                answer = f"Columns: {', '.join(dataframe.columns)}"
            else:
                answer = "Sorry, I can't answer that yet. Try asking about columns or averages."
        else:
            answer = "Please upload a file first."

        return JsonResponse({'answer': answer})
