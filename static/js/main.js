// Load data on page load
window.onload = function () {
    loadMetrics();
    loadSubscriptions();
    loadRenewals();
};

function loadMetrics() {
    fetch('/api/metrics')
        .then(res => res.json())
        .then(data => {
            document.getElementById('monthly-cost').textContent = '₹' + data.total_monthly.toFixed(2);
            document.getElementById('annual-cost').textContent = '₹' + data.total_annual.toFixed(2);
            document.getElementById('total-subs').textContent = data.total_subscriptions;
            document.getElementById('category-total').textContent = '₹' + data.total_monthly.toFixed(2);

            // Display categories
            const categoryDiv = document.getElementById('category-breakdown');
            categoryDiv.innerHTML = '';

            for (const [category, amount] of Object.entries(data.categories)) {
                const percentage = (amount / data.total_monthly * 100).toFixed(1);
                categoryDiv.innerHTML += `
                    <div>
                        <div class="flex justify-between mb-1">
                            <span class="text-gray-700">${category}</span>
                            <span class="text-gray-900 font-semibold">₹${amount.toFixed(2)} (${percentage}%)</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="bg-blue-600 h-2 rounded-full" style="width: ${percentage}%"></div>
                        </div>
                    </div>
                `;
            }
        });
}

function loadSubscriptions() {
    fetch('/api/subscriptions')
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById('subscriptions-table');
            tbody.innerHTML = '';

            data.forEach(sub => {
                tbody.innerHTML += `
                    <tr class="border-b hover:bg-gray-50">
                        <td class="py-3 px-4 font-semibold">${sub.name}</td>
                        <td class="py-3 px-4">₹${sub.amount}</td>
                        <td class="py-3 px-4 capitalize">${sub.billing_cycle}</td>
                        <td class="py-3 px-4">${sub.category}</td>
                        <td class="py-3 px-4">${sub.start_date}</td>
                        <td class="py-3 px-4">${sub.renewal_date}</td>
                        <td class="py-3 px-4">₹${sub.monthly_cost.toFixed(2)}</td>
                        <td class="py-3 px-4 text-center">
                            <button onclick="deleteSubscription(${sub.id})" class="text-red-600 hover:text-red-800">
                                <svg class="w-5 h-5 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                                </svg>
                            </button>
                        </td>
                    </tr>
                `;
            });
        });
}

function loadRenewals() {
    fetch('/api/renewals')
        .then(res => res.json())
        .then(data => {
            const renewalsDiv = document.getElementById('renewals-list');

            if (data.length === 0) {
                renewalsDiv.innerHTML = '<p class="text-gray-600">No renewals in the next 90 days</p>';
                return;
            }

            renewalsDiv.innerHTML = '';
            data.forEach(sub => {
                renewalsDiv.innerHTML += `
                    <div class="flex justify-between items-center p-3 bg-gray-50 rounded">
                        <div>
                            <p class="font-semibold text-gray-800">${sub.name}</p>
                            <p class="text-sm text-gray-600">${sub.renewal_date}</p>
                        </div>
                        <div class="text-right">
                            <p class="font-semibold text-gray-800">₹${sub.amount}</p>
                            <p class="text-sm text-orange-600">${sub.days_until} days</p>
                        </div>
                    </div>
                `;
            });
        });
}

function toggleAddForm() {
    const form = document.getElementById('add-form');
    form.classList.toggle('hidden');
}

function handleCategoryChange() {
    const category = document.getElementById('sub-category').value;
    const customField = document.getElementById('custom-category');

    if (category === 'Other') {
        customField.classList.remove('hidden');
    } else {
        customField.classList.add('hidden');
        customField.value = '';
    }
}

function saveSubscription() {
    const name = document.getElementById('sub-name').value;
    const amount = document.getElementById('sub-amount').value;
    const cycle = document.getElementById('sub-cycle').value;
    const category = document.getElementById('sub-category').value;
    const customCategory = document.getElementById('custom-category').value;
    const startDate = document.getElementById('sub-start-date').value;

    if (!name || !amount || !startDate) {
        alert('Please fill all required fields');
        return;
    }

    if (parseFloat(amount) <= 0) {
        alert('Amount must be greater than 0');
        return;
    }

    if (category === 'Other' && !customCategory.trim()) {
        alert('Please specify the category');
        return;
    }

    const data = {
        name: name,
        amount: parseFloat(amount),
        billing_cycle: cycle,
        category: category,
        customCategory: customCategory,
        start_date: startDate
    };

    fetch('/api/subscriptions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(() => {
            // Clear form
            document.getElementById('sub-name').value = '';
            document.getElementById('sub-amount').value = '';
            document.getElementById('sub-cycle').value = 'monthly';
            document.getElementById('sub-category').value = 'Entertainment';
            document.getElementById('custom-category').value = '';
            document.getElementById('sub-start-date').value = '';
            document.getElementById('custom-category').classList.add('hidden');

            // Hide form and reload data
            toggleAddForm();
            loadMetrics();
            loadSubscriptions();
            loadRenewals();
        });
}

function deleteSubscription(id) {
    if (!confirm('Are you sure you want to delete this subscription?')) {
        return;
    }

    fetch('/api/subscriptions/' + id, {
        method: 'DELETE'
    })
        .then(() => {
            loadMetrics();
            loadSubscriptions();
            loadRenewals();
        });
}

function exportToExcel() {
    window.location.href = '/api/export';
}
