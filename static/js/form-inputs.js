(() => {
	function formatCurrencyInput(input, preserveCaret = false) {
		const original = input.value;
		if (!original) return;

		const caret = preserveCaret ? input.selectionStart : null;
		const beforeCaret = caret === null ? '' : original.slice(0, caret);
		const digitsBeforeCaret = beforeCaret.replace(/\D/g, '').length;
		const caretWasAfterDecimal = beforeCaret.includes('.');
		const maxDecimals = Number(input.dataset.decimalPlaces || 0);
		const raw = original.replace(/[^\d.]/g, '');
		const decimalIndex = raw.indexOf('.');
		let integerPart = decimalIndex === -1 ? raw : raw.slice(0, decimalIndex);
		const hasDecimal = maxDecimals > 0 && decimalIndex !== -1;
		const fractionPart = hasDecimal
			? raw.slice(decimalIndex + 1).replace(/\D/g, '').slice(0, maxDecimals)
			: '';

		integerPart = integerPart.replace(/\D/g, '').replace(/^0+(?=\d)/, '');
		if (!integerPart && hasDecimal) integerPart = '0';

		const groupedInteger = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
		let formatted = groupedInteger;
		if (hasDecimal) formatted += `.${fractionPart}`;
		input.value = formatted;

		if (preserveCaret && caret !== null && input.setSelectionRange) {
			let newCaret = 0;
			if (caretWasAfterDecimal && formatted.includes('.')) {
				const integerDigits = integerPart.length;
				const fractionDigitsBeforeCaret = Math.max(0, digitsBeforeCaret - integerDigits);
				newCaret = formatted.indexOf('.') + 1 + fractionDigitsBeforeCaret;
			} else {
				let digitsSeen = 0;
				while (newCaret < formatted.length && digitsSeen < digitsBeforeCaret) {
					if (/\d/.test(formatted[newCaret])) digitsSeen++;
					newCaret++;
				}

	function initializeCurrencyInputs(root = document) {
		const inputs = [];
		if (root.matches?.('[data-currency-input]')) inputs.push(root);
		inputs.push(...(root.querySelectorAll?.('[data-currency-input]') || []));
		inputs.forEach(input => formatCurrencyInput(input));
	}
			}
			input.setSelectionRange(newCaret, newCaret);
		}
	}

	function initializeLocalDateTime(root = document) {
		const inputs = [];
		if (root.matches?.('[data-local-current]')) inputs.push(root);
		inputs.push(...(root.querySelectorAll?.('[data-local-current]') || []));

		const now = new Date();
		const pad = value => String(value).padStart(2, '0');
		const localDate = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
		const localTime = `${pad(now.getHours())}:${pad(now.getMinutes())}`;

		inputs.forEach(input => {
			if (input.value) return;
			if (input.dataset.localCurrent === 'date') input.value = localDate;
			if (input.dataset.localCurrent === 'time') input.value = localTime;
		});
	}

	window.initializeLocalDateTime = initializeLocalDateTime;

	document.addEventListener('input', event => {
		if (event.target.matches('[data-currency-input]')) {
			formatCurrencyInput(event.target, true);
		}
	});

	document.addEventListener('blur', event => {
		if (event.target.matches('[data-currency-input]')) {
			formatCurrencyInput(event.target);
		}
	}, true);

	document.addEventListener('submit', event => {
		event.target.querySelectorAll('[data-currency-input]').forEach(input => {
			input.value = input.value.replace(/,/g, '');
		});
	}, true);

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', () => {
			initializeLocalDateTime();
			initializeCurrencyInputs();
		});
	} else {
		initializeLocalDateTime();
		initializeCurrencyInputs();
	}
})();
