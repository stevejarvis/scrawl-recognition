package com.sajarvis.scrawl;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

/**
 * A fragment representing the main screen. This fragment is
 * either contained in a {@link ScreenListActivity} in two-pane mode (on
 * tablets) or a {@link ScreenDetailActivity} on handsets.
 */
public class ScreenDetailFragment extends Fragment {
	/**
	 * The fragment argument representing the item ID that this fragment
	 * represents.
	 */
	public static final String ARG_ITEM_ID = "item_id";

	/**
	 * Mandatory empty constructor for the fragment manager to instantiate the
	 * fragment (e.g. upon screen orientation changes).
	 */
	public ScreenDetailFragment() {
	}

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.fragment_screen_detail,
				container, false);

		// Show content as text in a TextView.
		((TextView) rootView.findViewById(R.id.screen_detail))
				.setText(getString(R.string.app_name));

		return rootView;
	}
}
