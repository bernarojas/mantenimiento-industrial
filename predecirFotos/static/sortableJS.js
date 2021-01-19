var lista = document.getElementById('lista');

Sortable.create(lista, {
    animation: 250,
    dragClass: "drag",
    group: "name",  // or { name: "...", pull: [true, false, 'clone', array], put: [true, false, array] }
	sort: true,  // sorting inside list
	delay: 0, // time in milliseconds to define when the sorting should start
	delayOnTouchOnly: false, // only delay if user is using touch
	touchStartThreshold: 0, // px, how many pixels the point should move before cancelling a delayed drag event
	disabled: false, // Disables the sortable if set to true.
	store: null,  // @see Store
	easing: "cubic-bezier(1, 0, 0, 1)", // Easing for animation. Defaults to null. See https://easings.net/ for examples.

	preventOnFilter: true, // Call `event.preventDefault()` when triggered `filter`


	swapThreshold: 1, // Threshold of the swap zone
	invertSwap: false, // Will always use inverted swap zone if set to true
	invertedSwapThreshold: 1, // Threshold of the inverted swap zone (will be set to swapThreshold value by default)
	direction: 'horizontal', // Direction of Sortable (will be detected automatically if not given)

	forceFallback: false,  // ignore the HTML5 DnD behaviour and force the fallback to kick in

	fallbackClass: "sortable-fallback",  // Class name for the cloned DOM Element when using forceFallback
	fallbackOnBody: false,  // Appends the cloned DOM Element into the Document's Body
	fallbackTolerance: 0, // Specify in pixels how far the mouse should move before it's considered as a drag.

	dragoverBubble: false,
	removeCloneOnHide: true, // Remove the clone element when it is not showing, rather than just hiding it
	emptyInsertThreshold: 5, // px, distance mouse must be from empty sortable to insert drag element into it
});