extends Label

var total_score = 0
@export var score_text : Label

func _on_balloon_popped(score):
	total_score += score
	print("Balloon popped! total score" + str(total_score))
	score_text.text = str("Score ", total_score)
