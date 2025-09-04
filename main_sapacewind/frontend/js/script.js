// scroll reveal
const io = new IntersectionObserver((entries)=>{
  for(const e of entries){
    if(e.isIntersecting){ e.target.classList.add('show'); io.unobserve(e.target); }
  }
},{ threshold:.08 });
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

// year in footer
document.getElementById('year').textContent = new Date().getFullYear();

// speech synthesis (fallback friendly)
function speak(text){
  if(!('speechSynthesis' in window)) return false;
  const utter = new SpeechSynthesisUtterance(text);
  utter.rate = 1;
  utter.pitch = 1;
  speechSynthesis.cancel();
  speechSynthesis.speak(utter);
  return true;
}

const speakBtn = document.getElementById('speakBtn');
if(speakBtn){
  speakBtn.addEventListener('click', ()=>{
    const ok = speak('Spacewind — Ideas at escape velocity');
    if(!ok){ speakBtn.textContent = 'Speech unsupported on this device'; speakBtn.disabled = true; }
  });
}

const demoBtn = document.getElementById('demoSpeak');
const speechStatus = document.getElementById('speechStatus');
if(demoBtn){
  demoBtn.addEventListener('click', ()=>{
    const ok = speak('Ideas at escape velocity.');
    if(speechStatus){
      speechStatus.textContent = ok ? 'Playing…' : 'Speech unsupported on this device';
      if(ok){
        const onEnd = ()=>{ speechStatus.textContent = 'Done.'; window.speechSynthesis.removeEventListener('end', onEnd, true); };
        window.speechSynthesis.addEventListener('end', onEnd, true);
      }
    }
  });
}

// contact forms: fake submit + toast
function handleForm(form){
  form.addEventListener('submit', (e)=>{
    e.preventDefault();
    // basic client validation
    const missing = [...form.querySelectorAll('[required]')].some(el=>!el.value.trim());
    const status = form.querySelector('.form-status');
    if(missing){
      status.textContent = 'Please fill out all required fields.';
      return;
    }
    status.textContent = 'Sent! We will get back to you shortly.';
    showToast('Thanks — we’ll be in touch!');
    form.reset();
  });
}
document.querySelectorAll('form').forEach(handleForm);

function showToast(msg){
  const toast = document.getElementById('toast') || document.createElement('div');
  toast.id = 'toast';
  toast.className = 'toast';
  toast.textContent = msg;
  toast.hidden = false;
  document.body.appendChild(toast);
  clearTimeout(showToast._t);
  showToast._t = setTimeout(()=> toast.hidden = true, 2600);
}

// Get modal elements
const privacyBtn = document.getElementById('privacyBtn');
const privacyModal = document.getElementById('privacyModal');
const closePrivacy = document.getElementById('closePrivacy');

const termsBtn = document.getElementById('termsBtn');
const termsModal = document.getElementById('termsModal');
const closeTerms = document.getElementById('closeTerms');

const cookiesBtn = document.getElementById('cookiesBtn');
const cookiesModal = document.getElementById('cookiesModal');
const closeCookies = document.getElementById('closeCookies');

// Open modals
if(privacyBtn) privacyBtn.onclick = () => { privacyModal.style.display = "block"; };
if(termsBtn) termsBtn.onclick = () => { termsModal.style.display = "block"; };
if(cookiesBtn) cookiesBtn.onclick = () => { cookiesModal.style.display = "block"; };

// Close modals when clicking the X
if(closePrivacy) closePrivacy.onclick = () => { privacyModal.style.display = "none"; };
if(closeTerms) closeTerms.onclick = () => { termsModal.style.display = "none"; };
if(closeCookies) closeCookies.onclick = () => { cookiesModal.style.display = "none"; };

// Close modal if user clicks outside the modal content
window.onclick = function(event) {
  if (event.target === privacyModal) privacyModal.style.display = "none";
  if (event.target === termsModal) termsModal.style.display = "none";
  if (event.target === cookiesModal) cookiesModal.style.display = "none";
};