const comments=document.querySelector('.comment');

function handleClick(e){
    const e_type=e.target.name;
    const pk=e.target.value;
    const tmp='.comment-edit-form-'+pk;
    const form=document.querySelector(tmp);
    
    if(e_type==="try-edit"){    
        form.classList.remove('hidden');
    }
    else if(e_type==="edit-back"){
        form.classList.add('hidden');
    }
}

function main(){
    comments.addEventListener("click", handleClick);
}

main();