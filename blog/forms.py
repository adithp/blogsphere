from  django import forms



from .models import Post


class PostForm(forms.ModelForm):
    
    
    class Meta():
        model = Post
        fields = ['title','content','thumbnail']
        widgets = {
            'title':forms.TextInput(attrs={
                'class':'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-slate-50 focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 focus:border-primary dark:focus:border-primary h-14 placeholder:text-slate-400 dark:placeholder:text-slate-500 p-[15px] text-base font-normal leading-normal transition-all',
                'id':"post-title",
                'placeholder':"Enter a catchy title"
            }),
            'thumbnail':forms.FileInput(attrs={
                'hidden':True,
                'id':'fileInput',
                'type':'file'
            })     
            }
    
   