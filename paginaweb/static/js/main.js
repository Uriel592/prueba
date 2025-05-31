const btnDelete = document.querySelectorAll('.btn-danger'); 

btnDelete.forEach((btn) => {
  btn.addEventListener('click', (e) => {
    if (!confirm('Are you sure you want to delete this contact?')) {
      e.preventDefault(); 
    }
  });
});
