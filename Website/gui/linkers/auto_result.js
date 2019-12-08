function expandTextarea(id) {
    var object = document.getElementById(id);
    if (object) {
        object.addEventListener('input', function() {
            this.style.overflow = 'hidden';
            this.style.height = 0;
            this.style.height = this.scrollHeight + 'px';
            console.log(this.style.height)
        }, false);
    } else {
        console.log("Id doesn't exists")
    }

}

expandTextarea('query-result');