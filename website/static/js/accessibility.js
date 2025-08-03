// Enhanced accessibility.js for voice navigation and screen reader support with Siri-like features

document.addEventListener('DOMContentLoaded', () => {
    // Voice navigation using SpeechRecognition API with continuous listening and speech synthesis feedback
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        const synth = window.speechSynthesis;

        const startBtn = document.createElement('button');
        startBtn.textContent = 'Start Voice Navigation';
        startBtn.style.position = 'fixed';
        startBtn.style.bottom = '10px';
        startBtn.style.right = '10px';
        startBtn.style.zIndex = '1000';
        startBtn.setAttribute('aria-label', 'Start voice navigation');
        document.body.appendChild(startBtn);

        let listening = false;

        // Function to get current language from localStorage or default to 'en'
        function getCurrentLanguage() {
            return localStorage.getItem('abilityHireLang') || 'en';
        }

        // Function to set recognition and synthesis language based on current language
        function setLanguage(lang) {
            if (lang === 'ar') {
                recognition.lang = 'ar-SA'; // Arabic (Saudi Arabia) - adjust if needed
            } else {
                recognition.lang = 'en-US';
            }
        }

        // Function to speak text with language support
        function speak(text) {
            if (synth.speaking) {
                synth.cancel();
            }
            const utterThis = new SpeechSynthesisUtterance(text);
            const lang = getCurrentLanguage();
            utterThis.lang = (lang === 'ar') ? 'ar-SA' : 'en-US';
            synth.speak(utterThis);
        }

        // Voice commands in English and Arabic
        const commands = {
            en: {
                home: ['home'],
                login: ['login', 'sign in', 'sign-in', 'open login'],
                signup: ['sign up', 'register', 'sign-up', 'open signup'],
                forget_password: ['forget password', 'forgot password', 'reset password', 'open forget password'],
                search_job: ['search job'],
                dashboard: ['dashboard'],
                user_training: ['user training'],
                about: ['about'],
                help: ['help'],
                profile: ['profile'],
                settings: ['settings'],
                post_job: ['post job', 'post jobs'],
                logout: ['logout', 'sign out'],
                help_me: ['help me', 'what can i say']
            },
            ar: {
                home: ['الرئيسية', 'الصفحة الرئيسية', 'البيت'],
                login: ['تسجيل الدخول', 'دخول', 'فتح تسجيل الدخول'],
                signup: ['إنشاء حساب', 'تسجيل', 'فتح إنشاء حساب'],
                forget_password: ['نسيت كلمة المرور', 'إعادة تعيين كلمة المرور', 'فتح نسيت كلمة المرور'],
                search_job: ['بحث عن وظيفة', 'ابحث عن وظيفة'],
                dashboard: ['لوحة التحكم', 'لوحة القيادة'],
                user_training: ['تدريب المستخدم'],
                about: ['حول', 'عن الموقع'],
                help: ['مساعدة', 'مساندة'],
                profile: ['الملف الشخصي', 'حسابي'],
                settings: ['الإعدادات', 'الضبط'],
                post_job: ['نشر وظيفة', 'نشر وظائف'],
                logout: ['تسجيل خروج', 'خروج'],
                help_me: ['ساعدني', 'ماذا يمكنني أن أقول']
            }
        };

        // Function to check if command matches any of the keywords in current language
        function matchCommand(command, keywords) {
            return keywords.some(keyword => command.includes(keyword));
        }

        // Update recognition language initially
        setLanguage(getCurrentLanguage());

        startBtn.addEventListener('click', () => {
            if (!listening) {
                // Create language selection dropdown
                const langSelect = document.createElement('select');
                langSelect.id = 'voiceLangSelect';
                const optionEn = document.createElement('option');
                optionEn.value = 'en';
                optionEn.textContent = 'English';
                const optionAr = document.createElement('option');
                optionAr.value = 'ar';
                optionAr.textContent = 'العربية';
                langSelect.appendChild(optionEn);
                langSelect.appendChild(optionAr);

                // Create confirm button
                const confirmBtn = document.createElement('button');
                confirmBtn.textContent = 'Start';
                confirmBtn.style.marginLeft = '10px';

                // Container for dropdown and button
                const container = document.createElement('div');
                container.id = 'voiceLangContainer';
                container.style.position = 'fixed';
                container.style.bottom = '50px';
                container.style.right = '10px';
                container.style.backgroundColor = 'white';
                container.style.border = '1px solid #ccc';
                container.style.padding = '5px';
                container.style.zIndex = '1001';
                container.style.display = 'flex';
                container.style.alignItems = 'center';
                container.appendChild(langSelect);
                container.appendChild(confirmBtn);

                document.body.appendChild(container);

                confirmBtn.addEventListener('click', () => {
                    const selectedLang = langSelect.value;
                    localStorage.setItem('abilityHireLang', selectedLang);
                    setLanguage(selectedLang);
                    recognition.start();
                    startBtn.textContent = (selectedLang === 'ar') ? 'بدء التنقل الصوتي' : 'Listening... Click to Stop';
                    speak((selectedLang === 'ar') ? 'تم بدء التنقل الصوتي. يمكنك قول أوامر مثل الرئيسية، تسجيل الدخول، إنشاء حساب، بحث عن وظيفة، لوحة التحكم، تدريب المستخدم، حول، مساعدة، الملف الشخصي، الإعدادات، نشر وظيفة، أو تسجيل خروج.' : 'Voice navigation started. You can say commands like Home, Login, Sign Up, Search Job, Dashboard, User Training, About, Help, Profile, Settings, Post Jobs, or Logout.');
                    listening = true;
                    // Remove the language selection UI
                    container.remove();
                });
            } else {
                recognition.stop();
                startBtn.textContent = (getCurrentLanguage() === 'ar') ? 'بدء التنقل الصوتي' : 'Start Voice Navigation';
                speak((getCurrentLanguage() === 'ar') ? 'تم إيقاف التنقل الصوتي.' : 'Voice navigation stopped.');
                listening = false;
            }
        });

        recognition.onresult = (event) => {
            const command = event.results[event.results.length - 1][0].transcript.toLowerCase().trim();
            console.log('Voice command received:', command);
            handleVoiceCommand(command);
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            speak((getCurrentLanguage() === 'ar') ? 'عذراً، لم أتمكن من سماع ذلك. يرجى المحاولة مرة أخرى.' : 'Sorry, I did not catch that. Please try again.');
        };

        recognition.onend = () => {
            if (listening) {
                recognition.start(); // Restart recognition for continuous listening
            }
        };

        function handleVoiceCommand(command) {
            const lang = getCurrentLanguage();
            const cmds = commands[lang];

            if (matchCommand(command, cmds.home)) {
                speak(lang === 'ar' ? 'جارٍ الانتقال إلى الصفحة الرئيسية.' : 'Navigating to home page.');
                window.location.href = '/';
            } else if (matchCommand(command, cmds.login)) {
                speak(lang === 'ar' ? 'جارٍ الانتقال إلى صفحة تسجيل الدخول.' : 'Navigating to login page.');
                window.location.href = '/login';
            } else if (matchCommand(command, cmds.signup)) {
                speak(lang === 'ar' ? 'جارٍ الانتقال إلى صفحة إنشاء حساب.' : 'Navigating to sign up page.');
                window.location.href = '/signup';
            } else if (matchCommand(command, cmds.forget_password)) {
                speak(lang === 'ar' ? 'جارٍ الانتقال إلى صفحة نسيت كلمة المرور.' : 'Navigating to forget password page.');
                window.location.href = '/forget_password';
            } else if (matchCommand(command, cmds.search_job)) {
                speak(lang === 'ar' ? 'جارٍ الانتقال إلى صفحة البحث عن وظيفة.' : 'Navigating to job search page.');
                window.location.href = '/searchjob';
            } else if (matchCommand(command, cmds.dashboard)) {
                speak(lang === 'ar' ? 'جارٍ التحقق من لوحة التحكم الخاصة بك.' : 'Checking your dashboard.');
                fetch('/api/get_user_role')
                    .then(response => response.json())
                    .then(data => {
                        if (data.role === 'publisher') {
                            speak(lang === 'ar' ? 'جارٍ الانتقال إلى لوحة تحكم الناشر.' : 'Navigating to publisher dashboard.');
                            window.location.href = '/publisherdashboard';
                        } else {
                            speak(lang === 'ar' ? 'جارٍ الانتقال إلى لوحة تحكم الباحث.' : 'Navigating to seeker dashboard.');
                            window.location.href = '/seekerdashboard';
                        }
                    })
                    .catch(() => {
                        speak(lang === 'ar' ? 'جارٍ الانتقال إلى لوحة تحكم الباحث.' : 'Navigating to seeker dashboard.');
                        window.location.href = '/seekerdashboard';
                    });
            } else if (matchCommand(command, cmds.user_training)) {
                speak(lang === 'ar' ? 'جارٍ الانتقال إلى صفحة تدريب المستخدم.' : 'Navigating to user training page.');
                window.location.href = '/user_training';
            } else if (matchCommand(command, cmds.about)) {
                speak(lang === 'ar' ? 'جارٍ الانتقال إلى صفحة حول.' : 'Navigating to about page.');
                window.location.href = '/about';
            } else if (matchCommand(command, cmds.help)) {
                speak(lang === 'ar' ? 'جارٍ الانتقال إلى صفحة المساعدة.' : 'Navigating to help page.');
                window.location.href = '/help';
            } else if (matchCommand(command, cmds.profile)) {
                speak(lang === 'ar' ? 'جارٍ الانتقال إلى ملفك الشخصي.' : 'Navigating to your profile.');
                window.location.href = '/profile';
            } else if (matchCommand(command, cmds.settings)) {
                speak(lang === 'ar' ? 'جارٍ الانتقال إلى الإعدادات.' : 'Navigating to settings.');
                window.location.href = '/setting';
            } else if (matchCommand(command, cmds.post_job)) {
                speak(lang === 'ar' ? 'جارٍ الانتقال إلى صفحة نشر الوظائف.' : 'Navigating to post jobs page.');
                window.location.href = '/postjobs';
            } else if (matchCommand(command, cmds.logout)) {
                speak(lang === 'ar' ? 'جارٍ تسجيل الخروج.' : 'Logging out.');
                window.location.href = '/logout';
            } else if (matchCommand(command, cmds.help_me)) {
                speak(lang === 'ar' ? 'يمكنك قول أوامر مثل الرئيسية، تسجيل الدخول، إنشاء حساب، نسيت كلمة المرور، بحث عن وظيفة، لوحة التحكم، تدريب المستخدم، حول، مساعدة، الملف الشخصي، الإعدادات، نشر وظيفة، أو تسجيل خروج.' : 'You can say commands like Home, Login, Sign Up, Forget Password, Search Job, Dashboard, User Training, About, Help, Profile, Settings, Post Jobs, or Logout.');
            } else {
                speak(lang === 'ar' ? 'الأمر غير معروف. يرجى المحاولة مرة أخرى أو قول ساعدني للمساعدة.' : 'Command not recognized. Please try again or say help me for assistance.');
            }
        }
    } else {
        console.warn('Speech Recognition API not supported in this browser.');
    }

    // Screen reader support: add ARIA roles and labels where needed
    const navs = document.getElementsByTagName('nav');
    for (let nav of navs) {
        nav.setAttribute('role', 'navigation');
        nav.setAttribute('aria-label', 'Main navigation');
    }

    // Add ARIA live region for dynamic announcements
    let liveRegion = document.getElementById('aria-live-region');
    if (!liveRegion) {
        liveRegion = document.createElement('div');
        liveRegion.id = 'aria-live-region';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.style.position = 'absolute';
        liveRegion.style.width = '1px';
        liveRegion.style.height = '1px';
        liveRegion.style.margin = '-1px';
        liveRegion.style.border = '0';
        liveRegion.style.padding = '0';
        liveRegion.style.overflow = 'hidden';
        liveRegion.style.clip = 'rect(0 0 0 0)';
        document.body.appendChild(liveRegion);
    }

    // Function to announce messages to screen reader
    function announce(message) {
        liveRegion.textContent = '';
        setTimeout(() => {
            liveRegion.textContent = message;
        }, 100);
    }

    // Example: announce page title on load
    announce(document.title);
});