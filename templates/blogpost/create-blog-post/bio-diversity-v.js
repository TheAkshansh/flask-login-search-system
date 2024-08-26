var blogForm = document.getElementById('blogForm');
var titleInput = document.getElementById('title');
var textInput = document.getElementById('text-input');
var blogPosts = document.getElementById('blogPosts');


var boldButton = document.getElementById('bold');
var italicButton = document.getElementById('italic');
var underlineButton = document.getElementById('underline');
var strikethroughButton = document.getElementById('strikethrough');
var superscriptButton = document.getElementById('superscript');
var subscriptButton = document.getElementById('subscript');
var insertOrderedListButton = document.getElementById('insertOrderedList');
var insertUnorderedListButton = document.getElementById('insertUnorderedList');
var createLinkButton = document.getElementById('createLink');
var foreColorInput = document.getElementById('foreColor');
var backColorInput = document.getElementById('backColor');
var fileInput = document.getElementById('file');


console.log(fileInput)
fileInput.addEventListener('change', (e) => {
    var file = e.target.files[0];
    console.log(file)
    if (file) {
        var reader = new FileReader();
        reader.onload = (e) => {
            var img = document.createElement('img');
            img.src = e.target.result;
            img.style.maxWidth = "100%";
            img.alt = "Uploaded Image";
            textInput.appendChild(img);
        };
        reader.readAsDataURL(file);
    }
});


boldButton.addEventListener('click', function() {
    document.execCommand('bold');
});

italicButton.addEventListener('click', function() {
    document.execCommand('italic');
});
underlineButton.addEventListener('click', () => document.execCommand('underline'));
strikethroughButton.addEventListener('click', () => document.execCommand('strikethrough'));
superscriptButton.addEventListener('click', () => document.execCommand('superscript'));
subscriptButton.addEventListener('click', () => document.execCommand('subscript'));
insertOrderedListButton.addEventListener('click', () => document.execCommand('insertOrderedList'));
insertUnorderedListButton.addEventListener('click', () => document.execCommand('insertUnorderedList'));
createLinkButton.addEventListener('click', () => {
    var url = prompt("Enter the URL:");
    if (url) {
        document.execCommand('createLink', false, url);
    }
});
console.log(formatBlockSelect)
// formatBlockSelect.addEventListener('change', () => {
//     document.execCommand('formatBlock', false, formatBlockSelect.value);
// });
// fontNameSelect.addEventListener('change', () => {
//     document.execCommand('fontName', false, fontNameSelect.value);
// });

// 
foreColorInput.addEventListener('change', function() {
    document.execCommand('foreColor', false, foreColorInput.value);
});

backColorInput.addEventListener('change', function() {
    document.execCommand('backColor', false, backColorInput.value);
});

function applyStyleToSelection(styleName, value) {
    let selectedText = window.getSelection();
    if (selectedText.rangeCount) {
        let range = selectedText.getRangeAt(0);
        let span = document.createElement('span');
        span.style[styleName] = value;
        range.surroundContents(span);
    }
}
// var input = document.getElementById('input');
//         input.addEventListener('change', function(e) {
//             console.log(e.target.files);
//         });


// Handle form submission
blogForm.addEventListener('submit', (e) => {
    e.preventDefault();

    var title = titleInput.value.trim();
    var content = textInput.innerHTML.trim();

    if (title && content) {
        const blogPosts = document.createElement('div');
        blogPosts.classList.add('blogPosts');
        
        const blogTitle = document.createElement('h3');
        blogTitle.textContent = title;

        const blogContent = document.createElement('div');
        blogContent.innerHTML = content;

        blogPosts.appendChild(blogTitle);
        blogPosts.appendChild(blogContent);

        blogPosts.appendChild(blogPosts);

        // Clear inputs
        titleInput.value = '';
        textInput.innerHTML = '';
    } else {
        alert('Please enter a title and content for your blog post.');
    }
});

var fontSizes = [1, 2, 3, 4, 5, 6, 7];
fontSizes.forEach(size => {
    var option = document.createElement('option');
    option.value = size;
    option.textContent = `Size ${size}`;
    fontSizeSelect.appendChild(option);
});
