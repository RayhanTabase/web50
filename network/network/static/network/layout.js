document.addEventListener('DOMContentLoaded', function() {
    //get all buttons with class profile_get
    //create function to get profile based on button id which would be username
      document.addEventListener('click', event =>{
          const element = event.target;
          // console.log("click occured")

          if(element.className === 'btn btn-link profile_get'){
              //let m = event.target.value
              // console.log("profile click")
              //console.log(m)
            window.location.replace(`http://127.0.0.1:8000/profile/${element.value}`)
          }
      })
});
