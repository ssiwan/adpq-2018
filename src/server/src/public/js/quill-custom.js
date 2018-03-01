        var toolbarOptions = [['bold', 'italic'], ];
        var toolbarOptions = [
          ['bold', 'italic', 'underline', 'strike'],        
          ['blockquote', 'code-block'],
          ['link', 'image'],
          [{ 'list': 'ordered'}, { 'list': 'bullet' }],
          [{ 'script': 'sub'}, { 'script': 'super' }],      
          [{ 'indent': '-1'}, { 'indent': '+1' }],          
          [{ 'direction': 'rtl' }],                         
          [{ 'color': [] }, { 'background': [] }],          
          [{ 'font': [] }],
          [{ 'align': [] }],
          ['clean']                                         
        ];
        var quill = new Quill('#longdesc', {
          modules: {
            toolbar: toolbarOptions
          },
          theme: 'snow'
        });
