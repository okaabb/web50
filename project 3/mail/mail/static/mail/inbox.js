document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email(-1));
  document.querySelector('form').onsubmit = send_email;
  // By default, load the inbox

  load_mailbox('inbox');
});
function send_email(event) {
  event.preventDefault();
  const receps = document.querySelector("#compose-recipients").value;
  const subj = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: receps,
      subject: subj,
      body: body,
    })
  })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      load_mailbox('sent');
    });
}
function compose_email(id) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  if (id == -1) {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }
  else {
    fetch(`/emails/${id}`)
      .then(response => response.json())
      .then(email => {
        let subject = email['subject'];
        if (subject.length > 3 && subject[0] === 'R' && subject[1] === 'e' && subject[2] === ':') subject = email['subject'];
        else subject = "Re: " + email['subject'];
        document.querySelector('#compose-recipients').value = email['sender'];
        document.querySelector('#compose-subject').value = subject;
        document.querySelector('#compose-body').value = `On ${email['timestamp']} ${email['sender']} wrote:  ${email['body']}`;
      });
  }
}
function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      for (let i = 0; i < emails.length; i++) {
        const content = `<div style="width:20%"> <strong>${emails[i]['sender']} </strong> </div>
                       <div style="width: 50%;"> ${emails[i]['subject']}  </div>
                       <div style="color: gray; text-align: right; width:30%"> ${emails[i]['timestamp']} </div>`
        const post = document.createElement('div');
        post.style.border = '2px solid black';
        post.style.display = "flex";
        post.style.marginBottom = "10px";
        post.style.padding = "5px";
        post.style.fontSize = "20px";
        if (emails[i]['read'] == true) {
          post.style.backgroundColor = "#ededed";
        }
        post.innerHTML = content;
        post.addEventListener('click', function () {
          console.log(`${emails[i]['id']} has been clicked!`);
          view_email(emails[i]['id'], mailbox);
          return;
        });
        document.querySelector('#emails-view').append(post);
      }
    });
}
function change_archive(id, flag) {
  console.log(flag);
  let flag2 = false;
  if (flag === false) flag2 = true;
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: flag2
    })
  })
}
function view_email(id, mailbox) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      console.log(email['archived']);
      content = `<strong> From: </strong> ${email['sender']}<br>
                       <strong>To: </strong> ${email['recipients']}<br>
                       <strong>Subject: </strong> ${email['subject']}<br>
                       <strong>TimeStamp: </strong> ${email['timestamp']}<br>
                       <button id="reply"> Reply </button><hr>`
      if (mailbox != 'sent') {
        content += `<form id="archive"> <input type="submit"`;
        if (email['archived'] === true) content += ` value="Unarchive"`;
        else content += `  value="Archive"`;
        content += `></form><hr>`
      }
      content += `${email['body']}`;
      document.querySelector('#emails-view').innerHTML = content;
      const el = document.querySelector('#reply');
      if (el) el.addEventListener('click', () => compose_email(id));
      const el2 = document.querySelector('#archive');
      if (el2) {
        el2.onsubmit = () => change_archive(id, email['archived']);
      }
    });
}
