document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-details-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  document.querySelector('#emails-view').innerHTML = '';

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-details-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach( email => {
      const container = document.createElement('div');
      container.className = 'border row p-3';
      if (email.read) {
        container.classList.add('text-muted', 'bg-light');
      }

      const link = document.createElement('a');
      link.className = 'text-decoration-none col-md-11';
      link.href = 'javascript:void(0)';
      link.innerHTML = `<div class="row">
                          <div class="col-md-4 h5">${email.sender}</div>
                          <div class="col-md-4">${email.subject}</div>
                          <div class="col-md-4 d-flex justify-content-end text-muted">${email.timestamp}</div>
                        </div>`
      container.append(link);
      link.onclick = () => view_email(email.id);

      const archiveContainer = document.createElement('div');
      archiveContainer.className = 'col-md-1 p-md-1';

      let archive;
      if (['inbox', 'archive'].includes(mailbox)) {
        archive = document.createElement('button');
        archive.className = 'btn btn-outline-warning btn-sm';
        if (mailbox == 'inbox') {
          archive.innerHTML = 'Archive';
          archive.onclick = () => archive_email(email.id);
        } else {
          archive.innerHTML = 'Unarchive';
          archive.onclick = () => unarchive_email(email.id);
        }
      } else {
        archive = document.createElement('span');
      }

      archiveContainer.append(archive);
      container.append(archiveContainer);

      document.querySelector('#emails-view').append(container);
    })
  })
  .catch (error => {
    console.log('Error:', error);
  });
}

function send_email() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  })
  .catch(error => {
    console.log('Error:', error);
  });

  load_mailbox('sent');
  return false;
}

function view_email(id) {

  // Show the email-details and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-details-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#email-details-view').innerHTML = '';
  document.querySelector('#email-details-view').innerHTML = '<hr>';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      const container = document.createElement('div');
      container.className = 'container';
      container.innerHTML = `<div><strong>From: </strong>${email.sender}</div>
                            <div><strong>To: </strong>${email.recipients}</div>
                            <div><strong>Subject: </strong>${email.subject}</div>
                            <div><strong>Timestamp: </strong>${email.timestamp}</div>
                            <input id="reply-button" class="mt-1 btn btn-outline-primary" type="button" value="Reply">
                            <hr>
                            <div style="white-space: pre-line;">${email.body}</div>`;

      document.querySelector('#email-details-view').append(container);
      document.querySelector('#reply-button').onclick = () => reply_email(email);
  });

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: 'True'
    })
  });
}


function archive_email(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })
  .then(() => load_mailbox('inbox'))
}


function unarchive_email(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })
  .then(() => load_mailbox('inbox'))
}


function reply_email(email) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-details-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = `${email.sender}`;
  if (  email.subject.startsWith('Re:')) {
    document.querySelector('#compose-subject').value = `${email.subject}`;
  } else {
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  }
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:
  ${email.body}`;
}