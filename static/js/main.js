function toggleFields(boxId, checkboxId) {
    var checkbox = document.getElementById(checkboxId);
    var box = document.getElementById(boxId);
    checkbox.onclick = function() {
      console.log(this);
      if (this.checked) {
        box.style['display'] = 'block';
      } else {
        box.style['display'] = 'none';
      }
    };
  }
  toggleFields('box', 'checkbox');
