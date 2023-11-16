extends Area2D

var clicks_to_pop : int = 3
var size_increase : float = 0.2
var score_to_give : int = 1

var float_to_top_speed : float = 2

signal popped

func _process(delta):
	position.y -= float_to_top_speed * delta
	if position.y < -100:
		queue_free()
	
	
func _on_input_event(viewport, event, shape_idx):
	#when clicked with left button
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		clicks_to_pop -= 1
		#increase size
		scale += Vector2(size_increase, size_increase)
		#when clicks_to_pop is 0, pop the balloon and emit signal
		if clicks_to_pop == 0:
			emit_signal("popped", score_to_give)
			queue_free()
