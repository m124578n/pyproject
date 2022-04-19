function show(){
    var pwd =document.querySelector(".pwd");
    var icon=document.querySelector(".icon");
     if(pwd.type==='password'){
       pwd.type="text";
       icon.classList.remove('fa-eye-slash');
       icon.classList.add('fa-eye');
       }
     else{
       pwd.type="password"
       icon.classList.remove('fa-eye');
       icon.classList.add('fa-eye-slash');
       } 
   }