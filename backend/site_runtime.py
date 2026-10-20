SITE_RUNTIME = r'''<script>
document.addEventListener('click', function(event) {
  var link = event.target.closest('.mobile-links a');
  if (link) link.closest('details').removeAttribute('open');
});
document.addEventListener('submit', async function(event) {
  var form = event.target;
  if (!form.matches('form[data-site-form]')) return;
  event.preventDefault();
  if (!form.reportValidity() || form.dataset.sending === 'true') return;
  var button = form.querySelector('[type=submit]');
  var status = form.querySelector('[role=status]');
  form.dataset.sending = 'true'; button.disabled = true;
  var tr = document.documentElement.lang === 'tr';
  status.textContent = tr ? 'Gönderiliyor…' : 'Sending…';
  try {
    var response = await fetch(form.action, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({fields:Object.fromEntries(new FormData(form))})});
    if (!response.ok) throw new Error('delivery');
    var result = await response.json();
    if (!result.id) throw new Error('missing confirmation');
    status.textContent = (tr ? 'Talebiniz kaydedildi. Takip no: ' : 'Your request was recorded. Reference: ') + result.id;
    form.reset();
  } catch(error) {
    status.textContent = tr ? 'Gönderilemedi. Bilgileriniz korunuyor; tekrar deneyin veya oteli arayın.' : 'Could not send. Your entries are preserved; retry or call the hotel.';
  } finally { form.dataset.sending = 'false'; button.disabled = false; }
});
</script>'''
