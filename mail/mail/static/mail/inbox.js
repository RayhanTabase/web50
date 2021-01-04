document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#main-mail-view').style.display = 'none'
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // triger submit new mail
  document.querySelector('#submit-mail').onclick = function(){
    let recipients = document.querySelector('#compose-recipients').value;
    let subject    = document.querySelector('#compose-subject').value;
    let body       = document.querySelector('#compose-body').value;

    if(recipients === ''){
      alert("recipient required")
    }else{
      submit_mail(recipients,subject,body);
    }
    
  };
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#main-mail-view').style.display = 'none'
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // fetch all mails for the mailbox
  fetch_all_emails(mailbox);


  document.querySelector("#mail-sender").innerHTML    = "";
  document.querySelector("#mail-subject").innerHTML    = "";
  document.querySelector("#mail-recipients").innerHTML = "";
  document.querySelector("#mail-timestamp").innerHTML  = "";
  document.querySelector("#mail-body").innerHTML      = "";

}

function submit_mail(recipients,subject,body){
  // console.log("submiting mail");

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response =>{
    // console.log(response)
    load_mailbox('sent');
    if(response.status === 400){
      alert("Invalid mail not sent")  
    }
    return response.json()
    
  }) 
}

function fetch_all_emails(mailbox){
  // console.log(`fetching emails ${mailbox}`)

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
              //  console.log(emails);

              
            emails.forEach((element) =>{
              
              let email_background = ""
              if (mailbox === "inbox"){
                if(element.read){
                  email_background = "lightgray "
                }else{
                  email_background = "white"
                }
              }else if(mailbox === "sent"){
                email_background = "palegreen"
  
              }else if (mailbox === "archive"){
                email_background = "cornsilk"
              }

              var email_item = document.createElement("div");
              email_item.className = `email_item`
              email_item.innerHTML = `
                <div class="container">
                  <button class="btn-outline" data-id="${element.id}" style="height:80px;width:100%;display: inline;background-color:${email_background};margin-bottom:10px">
                    <div style="display: inline;float:left;"> <strong>${element.sender}</strong></div>
                    <div style="display: inline;float:left;margin-left:20px">${element.subject}</div>

                    <div style="display: inline;float:right">${element.timestamp}</div>
                  </button>    
                </div>`;
          
              document.querySelector('#emails-view').appendChild(email_item);

              email_item.addEventListener('click',function(){     
                  show_email(element.id,element.archived,mailbox);
              });

            });
  });
}

function show_email(mail_id,status,mailbox){
  
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails-view').innerHTML = '';
  document.querySelector('#compose-view').style.display = 'none';
  
  let status_change = false
  
  if(status==false){
    status_change = true
    archive_text = "Archive"
    button_color = "primary"
  }else{
    status_change = false
    archive_text = "Unarchive"
    button_color = "secondary"
  }
  
  fetch_email(mail_id);
  
  //archive button and reply button
  document.querySelector('#mail-archive-button').innerHTML=""
  document.querySelector('#mail-reply-button').innerHTML=""

  if(mailbox!="sent"){
    document.querySelector('#mail-archive-button').innerHTML = `<button class="btn btn-sm btn-${button_color}" onclick="archive_email(${mail_id},${status_change})"> ${archive_text} </button>`
    document.querySelector('#mail-reply-button').innerHTML = `<button class="btn btn-outline-success style="bottom: inherit;" onclick="reply_email(${mail_id})"> Reply </button>`
  }
  
}


function fetch_email(mail_id){

  fetch(`/emails/${mail_id}`)
  .then(response => response.json())
  .then(mail => {
    // console.log(mail);
    document.querySelector('#main-mail-view').style.display = 'block';

    document.querySelector("#mail-sender").innerHTML    =mail.sender;
    document.querySelector("#mail-subject").innerHTML    = mail.subject;
    document.querySelector("#mail-recipients").innerHTML = mail.recipients;
    document.querySelector("#mail-timestamp").innerHTML  = mail.timestamp;
    document.querySelector("#mail-body").innerHTML      = mail.body;

    read_email(mail_id);

    });
}

function read_email(mail_id){

  fetch(`/emails/${mail_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  //console.log("email has been read")
}

function reply_email(mail_id){

  compose_email()

  //load mail
  fetch(`/emails/${mail_id}`)
  .then(response => response.json())
  .then(mail => {
   
    // Fill composition form

    let reply_subject = '';
    if(!mail.subject.startsWith("RE:")){
      reply_subject = `RE: ${mail.subject}`
      
    }else{
      reply_subject = mail.subject
    }
    document.querySelector('#compose-subject').value = reply_subject;


    let recipient = mail.sender;
    document.querySelector('#compose-recipients').value = `${recipient}`;

    let reply_body = mail.body;
    document.querySelector('#compose-body').value = `"On ${mail.timestamp} ${mail.sender} sent:`+`\n${reply_body}"`;
  })

}

function archive_email(mail_id,state){
  load_mailbox('inbox')

  fetch(`/emails/${mail_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: state
    })
  })
  
  window.location.reload()

  // let status_change = state;
  
  // if(state==true){
  //   status_change = false
  //   archive_text = "Unarchive"
  //   button_color = "secondary"
  // }else{
  //   status_change = true
  //   archive_text = "Archive"
  //   button_color = "primary"
  // }
  // document.querySelector('#archive-btn').innerHTML = `<button class="btn btn-sm btn-${button_color}" onclick="archive_email(${mail_id},${status_change})"> ${archive_text} </button>`;
   
}




