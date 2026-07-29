import { createShapeId } from 'tldraw'

const ID = createShapeId('qiaomu-counter-demo')
const TYPE = 'qiaomu-counter-v1'

function contains(shape, point) {
	return (
		point.x >= shape.x &&
		point.x <= shape.x + shape.props.w &&
		point.y >= shape.y &&
		point.y <= shape.y + shape.props.h
	)
}

export default function ({ editor, signal }) {
	if (!editor.getShape(ID)) {
		editor.createShape({ id: ID, type: TYPE, x: 120, y: 120, props: { w: 260, h: 140, count: 0 } })
	}

	function handleEvent(info) {
		if (info?.name !== 'pointer_down') return
		let point = null
		try {
			if (info.point && editor.screenToPage) point = editor.screenToPage(info.point)
		} catch {}
		point ??= editor.inputs?.currentPagePoint
		const shape = editor.getShape(ID)
		if (!point || !shape || !contains(shape, point)) return
		editor.updateShape({ id: ID, type: TYPE, props: { count: shape.props.count + 1 } })
	}

	editor.on('event', handleEvent)
	signal.addEventListener('abort', () => editor.off('event', handleEvent))
}
