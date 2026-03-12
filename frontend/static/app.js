const apiBase = "/api";
const authStorageKey = "cloudops_token";

const state = {
  token: window.localStorage.getItem(authStorageKey) || "",
  user: null,
};

const elements = {
  authView: document.getElementById("auth-view"),
  dashboardView: document.getElementById("dashboard-view"),
  loginForm: document.getElementById("login-form"),
  loginMessage: document.getElementById("login-message"),
  loginUsername: document.getElementById("login-username"),
  loginPassword: document.getElementById("login-password"),
  fillButtons: document.querySelectorAll(".fill-btn"),
  logoutButton: document.getElementById("logout-button"),
  userFullName: document.getElementById("user-full-name"),
  roleBadge: document.getElementById("role-badge"),
  adminPanel: document.getElementById("admin-panel"),
  readonlyMessage: document.getElementById("readonly-message"),
  tableSubtitle: document.getElementById("table-subtitle"),
  form: document.getElementById("service-form"),
  formMessage: document.getElementById("form-message"),
  tableMessage: document.getElementById("table-message"),
  servicesBody: document.getElementById("services-body"),
  total: document.getElementById("total-count"),
  healthy: document.getElementById("healthy-count"),
  warning: document.getElementById("warning-count"),
  critical: document.getElementById("critical-count"),
};

async function fetchJson(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (state.token) {
    headers.Authorization = `Bearer ${state.token}`;
  }

  const response = await fetch(`${apiBase}${path}`, {
    headers,
    ...options,
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    if (response.status === 401 && state.token) {
      clearSession();
      showLogin("Session expired. Please sign in again.");
    }
    throw new Error(errorBody.detail || "Request failed");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function isAdmin() {
  return state.user?.role === "admin";
}

function setRoleView() {
  const adminMode = isAdmin();
  elements.userFullName.textContent = `${state.user.full_name} (${state.user.username})`;
  elements.roleBadge.textContent = adminMode ? "Admin" : "Customer";
  elements.roleBadge.className = `role-badge ${adminMode ? "role-admin" : "role-customer"}`;
  elements.adminPanel.classList.toggle("hidden", !adminMode);
  elements.readonlyMessage.classList.toggle("hidden", adminMode);
  elements.tableSubtitle.textContent = adminMode
    ? "Update platform health in place and review operational notes."
    : "Read-only customer view for service visibility and operational transparency.";
}

function showLogin(message = "") {
  elements.authView.classList.remove("hidden");
  elements.dashboardView.classList.add("hidden");
  elements.loginMessage.textContent = message;
}

function showDashboard() {
  elements.authView.classList.add("hidden");
  elements.dashboardView.classList.remove("hidden");
  setRoleView();
}

function persistSession(token) {
  state.token = token;
  window.localStorage.setItem(authStorageKey, token);
}

function clearSession() {
  state.token = "";
  state.user = null;
  window.localStorage.removeItem(authStorageKey);
}

function setSummary(summary) {
  elements.total.textContent = summary.total;
  elements.healthy.textContent = summary.healthy;
  elements.warning.textContent = summary.warning;
  elements.critical.textContent = summary.critical;
}

function renderServices(services) {
  elements.servicesBody.innerHTML = "";

  if (!services.length) {
    const emptyRow = document.createElement("tr");
    emptyRow.innerHTML =
      '<td colspan="7">No services tracked yet. Add your first cloud component.</td>';
    elements.servicesBody.appendChild(emptyRow);
    return;
  }

  services.forEach((service) => {
    const row = document.createElement("tr");
    row.dataset.id = service.id;
    const safeName = escapeHtml(service.name);
    const safeEnvironment = escapeHtml(service.environment);
    const safeOwner = escapeHtml(service.owner);
    const safeEndpoint = service.endpoint
      ? `<a class="endpoint-link" href="${escapeHtml(service.endpoint)}" target="_blank" rel="noreferrer">${escapeHtml(service.endpoint)}</a>`
      : '<span class="muted-cell">N/A</span>';
    const safeNotes = escapeHtml(service.notes || "");

    if (isAdmin()) {
      row.innerHTML = `
        <td>${safeName}</td>
        <td>${safeEnvironment}</td>
        <td>${safeOwner}</td>
        <td>${safeEndpoint}</td>
        <td>
          <select data-field="status">
            <option value="Healthy" ${service.status === "Healthy" ? "selected" : ""}>Healthy</option>
            <option value="Warning" ${service.status === "Warning" ? "selected" : ""}>Warning</option>
            <option value="Critical" ${service.status === "Critical" ? "selected" : ""}>Critical</option>
          </select>
        </td>
        <td>
          <textarea data-field="notes" rows="2">${safeNotes}</textarea>
        </td>
        <td class="actions-cell">
          <button data-action="save" class="secondary-btn">Save</button>
          <button data-action="delete" class="danger-btn">Delete</button>
        </td>
      `;
    } else {
      row.innerHTML = `
        <td>${safeName}</td>
        <td>${safeEnvironment}</td>
        <td>${safeOwner}</td>
        <td>${safeEndpoint}</td>
        <td><span class="status-pill ${service.status.toLowerCase()}">${escapeHtml(service.status)}</span></td>
        <td>${safeNotes || '<span class="muted-cell">No notes</span>'}</td>
        <td><span class="muted-cell">View only</span></td>
      `;
    }

    elements.servicesBody.appendChild(row);
  });
}

async function refreshDashboard() {
  try {
    const [services, summary] = await Promise.all([
      fetchJson("/services"),
      fetchJson("/summary"),
    ]);
    renderServices(services);
    setSummary(summary);
    elements.tableMessage.textContent = "";
  } catch (error) {
    elements.tableMessage.textContent = error.message;
  }
}

async function restoreSession() {
  if (!state.token) {
    showLogin();
    return;
  }

  try {
    state.user = await fetchJson("/auth/me");
    showDashboard();
    await refreshDashboard();
  } catch (error) {
    showLogin("Please sign in to continue.");
  }
}

elements.fillButtons.forEach((button) => {
  button.addEventListener("click", () => {
    elements.loginUsername.value = button.dataset.username || "";
    elements.loginPassword.value = button.dataset.password || "";
  });
});

elements.loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  elements.loginMessage.textContent = "";

  try {
    const payload = {
      username: elements.loginUsername.value.trim(),
      password: elements.loginPassword.value,
    };
    const response = await fetchJson("/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    persistSession(response.access_token);
    state.user = response.user;
    elements.loginForm.reset();
    showDashboard();
    await refreshDashboard();
  } catch (error) {
    elements.loginMessage.textContent = error.message;
  }
});

elements.logoutButton.addEventListener("click", () => {
  clearSession();
  showLogin("You have been logged out.");
});

elements.form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!isAdmin()) {
    elements.formMessage.textContent = "Admin access required.";
    return;
  }

  const formData = new FormData(elements.form);
  const payload = Object.fromEntries(formData.entries());

  if (!payload.endpoint) {
    payload.endpoint = null;
  }
  if (!payload.notes) {
    payload.notes = null;
  }

  try {
    await fetchJson("/services", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    elements.form.reset();
    elements.formMessage.textContent = "Service created.";
    await refreshDashboard();
  } catch (error) {
    elements.formMessage.textContent = error.message;
  }
});

elements.servicesBody.addEventListener("click", async (event) => {
  if (!isAdmin()) {
    return;
  }

  const action = event.target.dataset.action;
  if (!action) {
    return;
  }

  const row = event.target.closest("tr");
  const serviceId = row?.dataset.id;
  if (!serviceId) {
    return;
  }

  try {
    if (action === "save") {
      await fetchJson(`/services/${serviceId}`, {
        method: "PUT",
        body: JSON.stringify({
          status: row.querySelector('[data-field="status"]').value,
          notes: row.querySelector('[data-field="notes"]').value || null,
        }),
      });
      elements.tableMessage.textContent = "Service updated.";
    }

    if (action === "delete") {
      await fetchJson(`/services/${serviceId}`, { method: "DELETE" });
      elements.tableMessage.textContent = "Service deleted.";
    }

    await refreshDashboard();
  } catch (error) {
    elements.tableMessage.textContent = error.message;
  }
});

restoreSession();
