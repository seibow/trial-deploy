document.addEventListener('DOMContentLoaded', function () {
  // すべての edit-delete-modal を処理
  document.querySelectorAll('.edit-delete-modal').forEach(function(modalElem) {

    // find elements inside modal
    const openConfirmBtn = modalElem.querySelector('.btn-open-confirm');
    const editLink = modalElem.querySelector('.btn-edit-link');
    const confirmForm = modalElem.querySelector('.confirm-delete-form');
    const backBtn = modalElem.querySelector('.btn-back');
    const cancelBtn = modalElem.querySelector('.btn-cancel');
    const initialMessage = modalElem.querySelector('.initial-message');
    const modalMessage = modalElem.querySelector('.confirm-message');

    // helper: switch to confirmation state
    function showConfirmState() {
      if (editLink) editLink.style.display = 'none';
      if (openConfirmBtn) openConfirmBtn.style.display = 'none';
      if (confirmForm) confirmForm.style.display = 'inline-block';
      if (backBtn) backBtn.style.display = 'inline-block';
      if (cancelBtn) cancelBtn.style.display = 'none';
      if (initialMessage) initialMessage.style.display = 'none';
      if (modalMessage) modalMessage.style.display = 'block';
    }

    // helper: restore initial state
    function restoreInitialState() {
      if (editLink) editLink.style.display = '';
      if (openConfirmBtn) openConfirmBtn.style.display = '';
      if (confirmForm) confirmForm.style.display = 'none';
      if (backBtn) backBtn.style.display = 'none';
      if (cancelBtn) cancelBtn.style.display = '';
      if (initialMessage) initialMessage.style.display = 'block';
      if (modalMessage) modalMessage.style.display = 'none';
    }

    // open confirm button
    if (openConfirmBtn) {
      openConfirmBtn.addEventListener('click', function (e) {
        e.preventDefault();
        showConfirmState();
      });
    }

    // back button
    if (backBtn) {
      backBtn.addEventListener('click', function (e) {
        e.preventDefault();
        restoreInitialState();
      });
    }

    // when modal hidden -> restore
    modalElem.addEventListener('hidden.bs.modal', function () {
      restoreInitialState();
    });

  });
});
