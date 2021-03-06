var toolbarOptions = [['bold', 'italic'], ];
var toolbarOptions = [
  ['bold', 'italic', 'underline', 'strike'],        
  ['blockquote'],
  ['link'],
  [{ 'list': 'ordered'}, { 'list': 'bullet' }],  
  [{ 'indent': '-1'}, { 'indent': '+1' }],                               
  [{ 'color': [] }],          
  [{ 'font': [] }],
  [{ 'align': [] }]                                
];
var quill = new Quill('#longdesc', {
  modules: {
	toolbar: toolbarOptions
  },
  theme: 'snow'
});



applyAccessibilityHacks();

		/**
* Applies accessibility to a quill editor
* TODO: Deprecate this method once this issue is resolved (https://github.com/quilljs/quill/issues/1173)
* @param {object}		editor		- A Quill editor instance
*/
function applyAccessibilityHacks() {

// Get ref to the toolbar
const query = quill.container.parentElement.getElementsByClassName('ql-toolbar');
if (query.length !== 1) {
// No toolbars found OR multiple which is not what we expect either
return;
}

const toolBar = query[0];


const buttons = toolBar.getElementsByTagName('button');
const selects = toolBar.getElementsByTagName('select');
/* const hrefs = toolBar.getElementsByTagName('a');

for (let i = 0; i < hrefs.length; i++) {
	const href = hrefs[i];
	const className = href.getAttribute('class').toLowerCase();
if (className.indexOf('preview') >= 0) {
	href.setAttribute('aria-label', 'Toggle preview');
	}

} */
for (let i = 0; i < selects.length; i++) {
	const select = selects[i];
	const className = select.getAttribute('class').toLowerCase();
if (className.indexOf('font') >= 0) {
	select.setAttribute('aria-label', 'Toggle font');
	}
else if (className.indexOf('picker') >= 0) {
	select.setAttribute('aria-label', 'Toggle picker');
	}
else if (className.indexOf('color') >= 0) {
	select.setAttribute('aria-label', 'Toggle color');
}
else if (className.indexOf('align') >= 0) {
	select.setAttribute('aria-label', 'Toggle align');
}
}

for (let i = 0; i < selects.length; i++) {
	const select = selects[i];
	const className = select.getAttribute('class').toLowerCase();
if (className.indexOf('font') >= 0) {
	select.setAttribute('aria-label', 'Toggle font');
	}
else if (className.indexOf('picker') >= 0) {
	select.setAttribute('aria-label', 'Toggle picker');
	}
else if (className.indexOf('color') >= 0) {
	select.setAttribute('aria-label', 'Toggle color');
}
else if (className.indexOf('align') >= 0) {
	select.setAttribute('aria-label', 'Toggle align');
}
// apply aria labels to base buttons
for (let i = 0; i < buttons.length; i++) {
const button = buttons[i];
const className = button.getAttribute('class').toLowerCase();

if (className.indexOf('bold') >= 0) {
	button.setAttribute('aria-label', 'Toggle bold text');
} else if (className.indexOf('italic') >= 0) {
	button.setAttribute('aria-label', 'Toggle italic text');
} else if (className.indexOf('underline') >= 0) {
	button.setAttribute('aria-label', 'Toggle underline text');
} 
else if (className.indexOf('strike') >= 0) {
	button.setAttribute('aria-label', 'Toggle strike text');
} 
else if (className.indexOf('link') >= 0) {
	button.setAttribute('aria-label', 'Toggle link text');
} 
else if (className.indexOf('blockquote') >= 0) {
	button.setAttribute('aria-label', 'Toggle blockquote text');
} else if (className.indexOf('list') >= 0 && button.value === 'ordered') {
	button.setAttribute('aria-label', 'Toggle ordered list');
} else if (className.indexOf('list') >= 0 && button.value === 'bullet') {
	button.setAttribute('aria-label', 'Toggle bulleted list');
}
else if (className.indexOf('indent') >= 0 && button.value === '-1') {
	button.setAttribute('aria-label', 'Toggle left indent');
}
else if (className.indexOf('indent') >= 0 && button.value === '+1') {
	button.setAttribute('aria-label', 'Toggle right indent');
}
else if (className.indexOf('direction') >= 0) {
	button.setAttribute('aria-label', 'Toggle direction');
}
else if (className.indexOf('font') >= 0) {
	button.setAttribute('aria-label', 'Toggle font');
}
else if (className.indexOf('picker') >= 0) {
	button.setAttribute('aria-label', 'Toggle picker');
}
else if (className.indexOf('color') >= 0) {
button.setAttribute('aria-label', 'Toggle color');
}
}

// Make pickers work with keyboard and apply aria labels
//FIXME: When you open a submenu with the keyboard and close it with the mouse by click somewhere else, the menu aria-hidden value is incorrectly left to `false`
const pickers = toolBar.getElementsByClassName('ql-picker');
for (let i = 0; i < pickers.length; i++) {
const picker = pickers[i];

const label = picker.getElementsByClassName('ql-picker-label')[0];
const optionsContainer = picker.getElementsByClassName('ql-picker-options')[0];
const options = optionsContainer.getElementsByClassName('ql-picker-item');

label.setAttribute('role', 'button');
label.setAttribute('aria-haspopup', 'true');
label.setAttribute('tabindex', '0');

if (i === 0) {
	// HACK ALERT
	// This is our size select box.. Works for us as we only have the one drop box
	label.setAttribute('aria-label', 'Font Size');
}

optionsContainer.setAttribute('aria-hidden', 'true');
optionsContainer.setAttribute('aria-label', 'submenu');

for (let x = 0; x < options.length; x++) {
	const item = options[x];
	item.setAttribute('tabindex', '0');
	item.setAttribute('role', 'button');

	// Read the css 'content' values and generate aria labels
	const size = window.getComputedStyle(item, ':before').content.replace('\"', '');
	item.setAttribute('aria-label', size);
	item.addEventListener('keyup', (e) => {
		if (e.keyCode === 13) {
			item.click();
			optionsContainer.setAttribute('aria-hidden', 'true');
		}
	});
}

label.addEventListener('keyup', (e) => {
	if (e.keyCode === 13) {
		label.click();
		optionsContainer.setAttribute('aria-hidden', 'false');
	}
});

}

}
}