document.addEventListener('DOMContentLoaded', function() {
    console.log('[auth] DOMContentLoaded: iniciando verificação de usuário logado.');
    fetchCurrentUser();
    // testLoginSuperuser();
    // logout();
    loadNav();
});

// Função para buscar dados do usuário autenticado
async function fetchCurrentUser() {
    try {
        // Tenta obter o token salvo (exemplo: localStorage, pode ser adaptado)
        const token = localStorage.getItem('authToken');
        console.log('[auth] Token encontrado:', token);
        if (!token) {
            console.log('[auth] Nenhum token encontrado. Usuário não logado.');
            setUserLoggedOut();
            return;
        }
        const response = await fetch('/api/user/me/', {
            headers: {
                'Authorization': 'Token ' + token,
                'Accept': 'application/json'
            }
        });
        console.log('[auth] Resposta da API /api/user/me/:', response.status);
        if (response.ok) {
            const user = await response.json();
            console.log('[auth] Usuário autenticado:', user);
            setUserLoggedIn(user);
        } else {
            console.log('[auth] Token inválido ou expirado.');
            setUserLoggedOut();
        }
    } catch (e) {
        console.log('[auth] Erro ao verificar usuário logado:', e);
        setUserLoggedOut();
    }
}

// Exibe info do usuário logado na navbar
function setUserLoggedIn(user) {
    const avatarDropdown = document.getElementById('navbarDropdownMenuAvatar');
    if (avatarDropdown) {
        avatarDropdown.querySelector('img').alt = user.first_name + ' ' + user.last_name;
        avatarDropdown.title = user.email;
    }
    // Exibe notificações e avatar
    document.querySelectorAll('.notifications-dropdown, .avatar-dropdown').forEach(el => {
        el.style.display = '';
    });
    // Esconde apenas os botões Login e Criar Conta, mantém Planos visível
    document.querySelectorAll('.action-buttons .btn').forEach(btn => {
        if (btn.textContent.trim() === 'Login' || btn.textContent.trim() === 'Criar Conta') {
            btn.style.display = 'none';
        } else {
            btn.style.display = '';
        }
    });
    console.log('[auth] Navbar atualizada para usuário logado:', user.email);
    // Exemplo: mostrar nome/email em algum lugar
    // document.getElementById('user-info').textContent = user.email;
}

// Esconde info do usuário logado na navbar
function setUserLoggedOut() {
    const avatarDropdown = document.getElementById('navbarDropdownMenuAvatar');
    if (avatarDropdown) {
        avatarDropdown.querySelector('img').alt = 'Visitante';
        avatarDropdown.title = '';
    }
    // Esconde notificações e avatar
    document.querySelectorAll('.notifications-dropdown, .avatar-dropdown').forEach(el => {
        el.style.display = 'none';
    });
    // Exibe todos os botões em action-buttons
    document.querySelectorAll('.action-buttons .btn').forEach(btn => {
        btn.style.display = '';
    });
    console.log('[auth] Navbar atualizada para visitante.');
    // document.getElementById('user-info').textContent = '';
}

// Função de login
async function login(email, password) {
    try {
        const response = await fetch('/api/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('authToken', data.token);
            console.log('[auth] Login bem-sucedido:', data);
            fetchCurrentUser();
            // Redireciona para a home após login
            window.location.href = '/web/';
            return data;
        } else {
            const err = await response.json();
            console.log('[auth] Falha no login:', err);
            return null;
        }
    } catch (e) {
        console.log('[auth] Erro no login:', e);
        return null;
    }
}

// Função de login de teste para superuser
async function testLoginSuperuser() {
    return await login('superuser@peacevs.com', '123456789');
}

// Função de logout
function logout() {
    localStorage.removeItem('authToken');
    setUserLoggedOut();
    console.log('[auth] Logout realizado. Token removido e navbar atualizada.');
}

// Função de signup (cadastro)
async function signup({ email, password, first_name, last_name, nome_perfil }) {
    try {
        const response = await fetch('/api/signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                email,
                password,
                first_name,
                last_name,
                nome_perfil
            })
        });
        if (response.ok) {
            const data = await response.json();
            console.log('[auth] Cadastro bem-sucedido:', data);
            // Login automático após cadastro
            await login(email, password);
            // Redireciona para a home após cadastro/login
            window.location.href = '/web/';
            return data;
        } else {
            const err = await response.json();
            console.log('[auth] Falha no cadastro:', err);
            return null;
        }
    } catch (e) {
        console.log('[auth] Erro no cadastro:', e);
        return null;
    }
}

function loadNav() {
    const logoutButton = document.getElementById('logoutButton');
    const signupForm = document.getElementById('signupForm');
    const loginForm = document.getElementById('loginForm');

    if (logoutButton) {
        logoutButton.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }

    if (signupForm) {
        signupForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const email = signupForm.querySelector('[name="email"], #formEmail')?.value;
            const password = signupForm.querySelector('[name="password"], #formPassword')?.value;
            const first_name = signupForm.querySelector('[name="first_name"], #formFirstName')?.value;
            const last_name = signupForm.querySelector('[name="last_name"], #formLastName')?.value;
            const nome_perfil = signupForm.querySelector('[name="nome_perfil"], #formNomePerfil')?.value;
            const user = await signup({ email, password, first_name, last_name, nome_perfil });
            if (user) {
                console.log('[auth] Cadastro realizado com sucesso:', user);
            } else {
                console.log('[auth] Falha no cadastro. Verifique os dados informados.');
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const email = loginForm.querySelector('[name="email"], #formEmail')?.value;
            const password = loginForm.querySelector('[name="password"], #formPassword')?.value;
            const user = await login(email, password);
            if (user) {
                console.log('[auth] Login realizado com sucesso:', user);
            } else {
                console.log('[auth] Falha no login. Verifique os dados informados.');
            }
        });
    }
}
